"""Cross-check the recovered certificate. Python 3.10+, standard library only."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFICATE = "two_sided_linear_m1024_L8_recovered_certificate.json"
BENCHMARK = Fraction(942809522, 10**9)
sys.path.insert(0, str(HERE))
try:
    import independent
    import smoothing_verify
except (ImportError, SyntaxError, OSError) as error:
    print(
        json.dumps(
            {"accepted": False, "input_error": f"checker import failed: {error}"}
        )
    )
    raise SystemExit(2) from error


def check_inventory() -> dict[str, object]:
    """Check the package manifest and return its exact reference results."""
    manifest = json.loads((HERE / "MANIFEST.json").read_text(encoding="utf-8"))
    seen = set()
    for member in manifest["files"]:
        name = member["path"]
        relative = Path(name)
        if (
            not isinstance(name, str)
            or relative.is_absolute()
            or ".." in relative.parts
            or relative.as_posix() != name
            or name in seen
        ):
            raise ValueError("unsafe or duplicate manifest path")
        seen.add(name)
        target = (HERE / relative).resolve()
        if not target.is_relative_to(HERE.resolve()):
            raise ValueError("manifest path escapes the package")
        content = target.read_bytes()
        if len(content) != member["bytes"]:
            raise ValueError(f"manifest size mismatch: {name}")
        if hashlib.sha256(content).hexdigest() != member["sha256"]:
            raise ValueError(f"manifest hash mismatch: {name}")
    required = {
        CERTIFICATE,
        "verify.py",
        "independent.py",
        "smoothing_verify.py",
        "EXPECTED_RESULTS.json",
    }
    if not required <= seen:
        raise ValueError("manifest omits a required verification input")
    expected = json.loads((HERE / "EXPECTED_RESULTS.json").read_text(encoding="utf-8"))
    if not isinstance(expected, dict) or set(expected) != {
        "certificate",
        "research",
        "independent",
    }:
        raise ValueError("malformed expected results")
    if expected["certificate"] != CERTIFICATE:
        raise ValueError("unexpected bundled certificate name")
    return expected


def check_one(path: Path) -> dict[str, object]:
    """Run both existing implementations without trusting saved success flags."""
    direct = independent.verify_certificate(path, comparator=BENCHMARK)
    research = smoothing_verify.load_and_verify(path, mode="two-sided").to_dict()
    research.pop("gamma_float_diagnostic_only", None)
    comparisons = (
        ("a", "energy_constant_a"),
        ("b", "boundary_constant_b"),
        ("ab", "gamma_squared_ab"),
        ("declared_bound", "declared_bound"),
    )
    agreement = all(
        Fraction(direct[left]) == Fraction(research[right])
        for left, right in comparisons
    )
    agreement = agreement and (direct["accepted_feasible"] == research["checks_passed"])
    reasons = []
    if not agreement:
        reasons.append("independent checking implementations disagree")
    if not research["checks_passed"] or not direct["accepted_feasible"]:
        reasons.append("finite certificate is mathematically rejected")
    if not direct["beats_target"]:
        reasons.append("certificate does not strictly beat the fixed benchmark")
    return {
        "accepted": not reasons,
        "agreement": agreement,
        "research": research,
        "independent": direct,
        "failures": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "certificate",
        type=Path,
        nargs="?",
        help="optional certificate path, relative to the current directory",
    )
    args = parser.parse_args()
    try:
        expected = check_inventory()
        path = args.certificate or HERE / CERTIFICATE
        output = check_one(path)
        if path.resolve() == (HERE / CERTIFICATE).resolve():
            actual = {
                "certificate": CERTIFICATE,
                "research": output["research"],
                "independent": output["independent"],
            }
            if actual != expected:
                raise ValueError("fresh results disagree with bundled exact reference")
        output["manifest_checked"] = True
    except smoothing_verify.NonpositiveDeclaredBoundError as error:
        print(json.dumps({"accepted": False, "failures": [str(error)]}, sort_keys=True))
        return 1
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        OverflowError,
    ) as error:
        print(
            json.dumps({"accepted": False, "input_error": str(error)}, sort_keys=True)
        )
        return 2
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0 if output["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
