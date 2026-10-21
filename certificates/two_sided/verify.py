"""Portable exact two-sided certificate checker. Python 3.10+, standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Isolated Python omits the script directory; import only our explicit sibling.
sys.path.insert(0, str(HERE))
from smoothing_verify import NonpositiveDeclaredBoundError, load_and_verify  # noqa: E402


def check_one(path: Path) -> dict[str, object]:
    result = load_and_verify(path, mode="two-sided").to_dict()
    result.pop("gamma_float_diagnostic_only", None)
    return {"certificate": path.name, **result}


def check_inventory() -> None:
    document = json.loads((HERE / "MANIFEST.json").read_text(encoding="utf-8"))
    for member in document["files"]:
        relative = Path(member["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("unsafe manifest path")
        content = (HERE / relative).read_bytes()
        if len(content) != member["bytes"]:
            raise ValueError(f"manifest size mismatch: {relative}")
        if hashlib.sha256(content).hexdigest() != member["sha256"]:
            raise ValueError(f"manifest hash mismatch: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path, nargs="?")
    parser.add_argument("--all", action="store_true", help="check all seven bundled certificates")
    args = parser.parse_args()
    if args.all and args.certificate is not None:
        parser.error("choose a certificate or --all")
    try:
        if args.all:
            check_inventory()
            expected = json.loads((HERE / "EXPECTED_RESULTS.json").read_text(encoding="utf-8"))
            names = [reference["certificate"] for reference in expected["results"]]
            bundled = {path.name for path in HERE.glob("*_certificate.json")}
            if (
                len(names) != 7
                or len(set(names)) != 7
                or set(names) != bundled
                or any(Path(name).name != name for name in names)
            ):
                raise ValueError(
                    "expected results must cover the seven distinct bundled certificates"
                )
            results = []
            for reference in expected["results"]:
                actual = check_one(HERE / reference["certificate"])
                results.append(actual)
                if actual != reference:
                    raise ValueError(f"expected exact result mismatch: {reference['certificate']}")
            if len(results) != 7:
                raise ValueError("expected exactly seven bundled certificates")
            passed = all(result["checks_passed"] for result in results)
            output = {"checks_passed": passed, "manifest_checked": True, "results": results}
        else:
            path = args.certificate or HERE / "two_sided_linear_m1024_L8_certificate.json"
            output = check_one(path)
            passed = bool(output["checks_passed"])
    except NonpositiveDeclaredBoundError as error:
        print(json.dumps({"checks_passed": False, "failures": [str(error)]}, sort_keys=True))
        return 1
    except (OSError, ValueError, TypeError, KeyError, IndexError, OverflowError) as error:
        print(json.dumps({"checks_passed": False, "input_error": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
