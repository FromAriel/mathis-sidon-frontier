"""Independent standard-library checker. Copy this file into a certificate packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

BASELINE_SHA256 = "5c441ae04ec2ad404832d9ffa77a2d0c61b07648202aed2805829363e883da77"
MATERIAL_GAIN = Fraction("1/1000000000000")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_fraction(value):
    if not isinstance(value, str):
        raise ValueError("fractions must be strings")
    return Fraction(value)


def verify(data):
    expected = {
        "format_version",
        "block_size",
        "window_length",
        "mixing",
        "kernels",
        "boundary",
        "declared_bound",
    }
    if set(data) != expected or data["format_version"] != (
        "mathis.research.sidon.smoothing_certificate.v1"
    ):
        raise ValueError("certificate schema mismatch")
    m, length = data["block_size"], data["window_length"]
    if type(m) is not int or type(length) is not int or m < 1 or length < 1:
        raise ValueError("invalid dimensions")
    mixing = [read_fraction(x) for x in data["mixing"]]
    kernels = [[read_fraction(x) for x in row] for row in data["kernels"]]
    boundary = [[read_fraction(x) for x in row] for row in data["boundary"]]
    if not mixing or len(mixing) != len(kernels) or len(mixing) != len(boundary):
        raise ValueError("component shape mismatch")
    if min(mixing) < 0 or sum(mixing) != 1:
        raise ValueError("invalid mixing")
    n = m * length
    for p, w in zip(kernels, boundary, strict=True):
        if len(p) != m or len(w) != n:
            raise ValueError("row shape mismatch")
        if min(p) < 0 or sum(p) != 1 or p != p[::-1]:
            raise ValueError("invalid kernel")
    slacks = []
    for q in range(n + 1):
        total = Fraction(0)
        for r, lam in enumerate(mixing):
            for i in range(m):
                weight = boundary[r][q + i] if q + i < n else Fraction(1)
                total += lam * kernels[r][i] * weight
        slacks.append(total - 1)
    if min(slacks) < 0:
        raise ValueError("covering inequality failed")
    a = m * sum(mixing[r] * sum(p * p for p in kernels[r]) for r in range(len(mixing)))
    b = 1 + 2 * (
        sum(mixing[r] * sum(w * w for w in boundary[r]) for r in range(len(mixing))) / m - length
    )
    declared = read_fraction(data["declared_bound"])
    if b <= 0 or declared != Fraction(9435, 10000) or a * b >= declared * declared:
        raise ValueError("coefficient or declared bound failed")
    return {"a": a, "b": b, "ab": a * b, "slacks": slacks, "dimensions": [len(mixing), m, length]}


def compare_values(old, new):
    gain = old - new
    with localcontext() as ctx:
        ctx.prec = 60
        value = Decimal(new.numerator) / new.denominator
    return {
        "status": "exact-improvement-certified" if gain > 0 else "no-exact-improvement",
        "material": gain >= MATERIAL_GAIN,
        "ab_baseline": str(old),
        "ab_candidate": str(new),
        "exact_gain_ab": str(gain),
        "ab_decimal_diagnostic": str(value),
        "material_threshold": str(MATERIAL_GAIN),
    }


def verify_pair(candidate, baseline):
    candidate, baseline = Path(candidate), Path(baseline)
    if digest(baseline) != BASELINE_SHA256:
        raise ValueError("baseline hash mismatch")
    old = verify(json.loads(baseline.read_text(encoding="utf-8")))
    new = verify(json.loads(candidate.read_text(encoding="utf-8")))
    if old["dimensions"] != [16, 32, 4] or new["dimensions"] != [16, 32, 4]:
        raise ValueError("frozen dimensions mismatch")
    result = compare_values(old["ab"], new["ab"])
    result.update(
        {
            "candidate_sha256": digest(candidate),
            "baseline_sha256": digest(baseline),
            "a": str(new["a"]),
            "b": str(new["b"]),
            "covering_slacks": [str(x) for x in new["slacks"]],
            "covering_count": len(new["slacks"]),
            "checks_passed": True,
        }
    )
    return result


def verify_manifest(path):
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data["files"]
    names = [entry["path"] for entry in files]
    required = {"CERTIFICATE.json", "BASELINE.json", "verify.py"}
    if len(names) != len(set(names)) or not required <= set(names):
        raise ValueError("invalid packet manifest inventory")
    for entry in files:
        if Path(entry["path"]).name != entry["path"]:
            raise ValueError("manifest requires flat paths")
        member = path.parent / entry["path"]
        if member.stat().st_size != entry["bytes"] or digest(member) != entry["sha256"]:
            raise ValueError(f"manifest mismatch: {entry['path']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate", type=Path, default=Path(__file__).with_name("CERTIFICATE.json")
    )
    parser.add_argument("--baseline", type=Path, default=Path(__file__).with_name("BASELINE.json"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = args.manifest
        if manifest is None and args.candidate.parent == Path(__file__).parent:
            manifest = Path(__file__).with_name("MANIFEST.json")
        if manifest is not None:
            verify_manifest(manifest)
        result = verify_pair(args.candidate, args.baseline)
        code = 0 if result["status"] != "no-exact-improvement" else 1
    except (ValueError, KeyError, TypeError, OSError, ZeroDivisionError) as error:
        result = {"status": "verification-failed", "checks_passed": False, "error": str(error)}
        code = 2
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
