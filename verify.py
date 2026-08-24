#!/usr/bin/env python3
"""Standalone exact verifier for the Sidon Frontier R9 certificate.

This program uses only the Python standard library. Every proof-bearing
calculation uses ``fractions.Fraction``. Decimal values are diagnostic output
only; the record comparison is performed on the exact squared constants.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

CERTIFICATE_SCHEMA = "mathis.research.sidon.smoothing_certificate.v1"
CERTIFICATE_SHA256 = "85e9e878cf3d129fdccbd74d54fbb88c1a6a0c0e6f6b50f6c7064826046b0e75"
HOU_ZHAO_ARXIV = "arXiv:2607.01169v2"
HOU_ZHAO_GAMMA_DISPLAY = "0.9434925907135450"
HOU_ZHAO_AB = Fraction(
    34772588622318632383981521978715331189177469643597175481323,
    39062500000000000000000000000000000000000000000000000000000,
)
EXPECTED_DECLARED_BOUND = Fraction(1887, 2000)
ALLOWED_FIELDS = {
    "format_version",
    "block_size",
    "window_length",
    "declared_bound",
    "mixing",
    "kernels",
    "boundary",
}


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains a duplicate key."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse_fraction(raw: object, origin: str) -> Fraction:
    if not isinstance(raw, str):
        raise ValueError(f"{origin}: expected a canonical rational string")
    if "/" in raw:
        pieces = raw.split("/")
        if len(pieces) != 2:
            raise ValueError(f"{origin}: malformed rational")
        numerator_text, denominator_text = pieces
        if not numerator_text.lstrip("-").isdigit() or not denominator_text.isdigit():
            raise ValueError(f"{origin}: malformed rational")
        denominator = int(denominator_text)
        if denominator <= 0:
            raise ValueError(f"{origin}: denominator must be positive")
        value = Fraction(int(numerator_text), denominator)
    elif raw.lstrip("-").isdigit():
        value = Fraction(int(raw), 1)
    else:
        raise ValueError(f"{origin}: malformed rational")
    if str(value) != raw:
        raise ValueError(f"{origin}: rational is not in reduced canonical form")
    return value


@dataclass(frozen=True)
class Certificate:
    block_size: int
    window_length: int
    declared_bound: Fraction
    mixing: tuple[Fraction, ...]
    kernels: tuple[tuple[Fraction, ...], ...]
    boundary: tuple[tuple[Fraction, ...], ...]

    @property
    def kernel_count(self) -> int:
        return len(self.mixing)

    @property
    def boundary_length(self) -> int:
        return self.block_size * self.window_length


@dataclass(frozen=True)
class Verification:
    a: Fraction
    b: Fraction
    ab: Fraction
    slacks: tuple[Fraction, ...]
    failures: tuple[str, ...]


def load_certificate(path: Path) -> tuple[Certificate, str]:
    raw_bytes = path.read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    if digest != CERTIFICATE_SHA256:
        raise ValueError(
            f"certificate SHA-256 mismatch: expected {CERTIFICATE_SHA256}, received {digest}"
        )
    payload = json.loads(
        raw_bytes.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_float=lambda value: (_ for _ in ()).throw(
            ValueError(f"floating-point JSON value is forbidden: {value}")
        ),
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON value is forbidden: {value}")
        ),
    )
    if not isinstance(payload, dict):
        raise ValueError("certificate document must be a JSON object")
    unknown = set(payload) - ALLOWED_FIELDS
    missing = ALLOWED_FIELDS - set(payload)
    if unknown:
        raise ValueError(f"unknown certificate fields: {sorted(unknown)}")
    if missing:
        raise ValueError(f"missing certificate fields: {sorted(missing)}")
    if payload["format_version"] != CERTIFICATE_SCHEMA:
        raise ValueError(f"format_version must be {CERTIFICATE_SCHEMA}")

    block_size = payload["block_size"]
    window_length = payload["window_length"]
    if type(block_size) is not int or block_size < 1:
        raise ValueError("block_size must be a positive integer")
    if type(window_length) is not int or window_length < 1:
        raise ValueError("window_length must be a positive integer")

    mixing_raw = payload["mixing"]
    kernels_raw = payload["kernels"]
    boundary_raw = payload["boundary"]
    if not isinstance(mixing_raw, list):
        raise ValueError("mixing must be a list")
    if not isinstance(kernels_raw, list):
        raise ValueError("kernels must be a list")
    if not isinstance(boundary_raw, list):
        raise ValueError("boundary must be a list")

    mixing = tuple(
        _parse_fraction(value, f"mixing[{index}]") for index, value in enumerate(mixing_raw)
    )
    kernels: list[tuple[Fraction, ...]] = []
    for r, row in enumerate(kernels_raw):
        if not isinstance(row, list):
            raise ValueError(f"kernels[{r}] must be a list")
        kernels.append(
            tuple(
                _parse_fraction(value, f"kernels[{r}][{index}]") for index, value in enumerate(row)
            )
        )
    boundary: list[tuple[Fraction, ...]] = []
    for r, row in enumerate(boundary_raw):
        if not isinstance(row, list):
            raise ValueError(f"boundary[{r}] must be a list")
        boundary.append(
            tuple(
                _parse_fraction(value, f"boundary[{r}][{index}]") for index, value in enumerate(row)
            )
        )

    if not mixing:
        raise ValueError("certificate must contain at least one kernel")
    if len(kernels) != len(mixing) or len(boundary) != len(mixing):
        raise ValueError("mixing, kernel, and boundary counts must agree")
    expected_boundary_length = block_size * window_length
    for r, kernel in enumerate(kernels):
        if len(kernel) != block_size:
            raise ValueError(f"kernels[{r}] must contain {block_size} entries")
    for r, row in enumerate(boundary):
        if len(row) != expected_boundary_length:
            raise ValueError(f"boundary[{r}] must contain {expected_boundary_length} entries")

    declared_bound = _parse_fraction(payload["declared_bound"], "declared_bound")
    if declared_bound != EXPECTED_DECLARED_BOUND:
        raise ValueError(f"declared_bound must be the frozen value {EXPECTED_DECLARED_BOUND}")
    return (
        Certificate(
            block_size=block_size,
            window_length=window_length,
            declared_bound=declared_bound,
            mixing=mixing,
            kernels=tuple(kernels),
            boundary=tuple(boundary),
        ),
        digest,
    )


def _weight(certificate: Certificate, kernel_index: int, index: int) -> Fraction:
    if index < certificate.boundary_length:
        return certificate.boundary[kernel_index][index]
    return Fraction(1, 1)


def verify(certificate: Certificate) -> Verification:
    failures: list[str] = []
    if any(weight < 0 for weight in certificate.mixing):
        failures.append("a mixing weight is negative")
    if sum(certificate.mixing, Fraction()) != 1:
        failures.append("mixing weights do not sum exactly to one")

    for r, kernel in enumerate(certificate.kernels):
        if any(value < 0 for value in kernel):
            failures.append(f"kernel {r} contains a negative entry")
        if sum(kernel, Fraction()) != 1:
            failures.append(f"kernel {r} does not sum exactly to one")
        if any(
            kernel[index] != kernel[certificate.block_size - 1 - index]
            for index in range(certificate.block_size)
        ):
            failures.append(f"kernel {r} is not exactly symmetric")

    slacks: list[Fraction] = []
    for q in range(certificate.boundary_length + 1):
        mass = Fraction()
        for r, mixing_weight in enumerate(certificate.mixing):
            for i, kernel_weight in enumerate(certificate.kernels[r]):
                mass += mixing_weight * kernel_weight * _weight(certificate, r, q + i)
        slack = mass - 1
        slacks.append(slack)
        if slack < 0:
            failures.append(f"covering constraint q={q} has negative slack {slack}")

    kernel_energy = Fraction()
    boundary_energy = Fraction()
    for r, mixing_weight in enumerate(certificate.mixing):
        kernel_energy += mixing_weight * sum(
            (value * value for value in certificate.kernels[r]), Fraction()
        )
        boundary_energy += mixing_weight * sum(
            (value * value for value in certificate.boundary[r]), Fraction()
        )
    a = certificate.block_size * kernel_energy
    b = 1 + 2 * (boundary_energy / certificate.block_size - certificate.window_length)
    if b <= 0:
        failures.append(f"boundary constant b is not positive: {b}")
    ab = a * b
    if ab >= certificate.declared_bound**2:
        failures.append("candidate ab is not below the declared bound squared")
    if ab >= HOU_ZHAO_AB:
        failures.append("candidate ab does not improve the exact Hou-Zhao baseline")
    return Verification(
        a=a,
        b=b,
        ab=ab,
        slacks=tuple(slacks),
        failures=tuple(failures),
    )


def _decimal_sqrt(value: Fraction, precision: int = 60) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        return (Decimal(value.numerator) / Decimal(value.denominator)).sqrt()


def _display_fraction(value: Fraction, verbose: bool) -> str:
    text = str(value)
    if verbose or len(text) <= 180:
        return text
    return f"{text[:84]}...{text[-84:]} ({len(text)} characters; use --verbose for full value)"


def print_report(
    path: Path,
    digest: str,
    certificate: Certificate,
    result: Verification,
    *,
    verbose: bool,
) -> None:
    minimum_slack = min(result.slacks)
    minimum_index = result.slacks.index(minimum_slack)
    positive_slacks = [value for value in result.slacks if value > 0]
    least_positive = min(positive_slacks) if positive_slacks else None
    equality_indices = [index for index, value in enumerate(result.slacks) if value == 0]
    candidate_gamma = _decimal_sqrt(result.ab)
    baseline_gamma = _decimal_sqrt(HOU_ZHAO_AB)
    gamma_improvement = baseline_gamma - candidate_gamma

    print("SIDON FRONTIER CERTIFICATE - EXACT VERIFICATION")
    print("=" * 54)
    print(f"Certificate file: {path.name}")
    print(f"Certificate SHA-256: {digest}")
    print(f"Schema: {CERTIFICATE_SCHEMA}")
    print()
    print("Theorem parameters")
    print(f"  R (kernels): {certificate.kernel_count}")
    print(f"  m (kernel length): {certificate.block_size}")
    print(f"  L (boundary depth): {certificate.window_length}")
    print(f"  boundary entries per kernel: {certificate.boundary_length}")
    print(f"  covering constraints: {len(result.slacks)}")
    print()
    print("[1/7] Strict certificate parse and frozen hash ........ PASS")
    print("[2/7] Mixing weights nonnegative; exact sum = 1 ...... PASS")
    print(f"[3/7] {certificate.kernel_count} kernels nonnegative, normalized, symmetric .. PASS")
    print(f"[4/7] {len(result.slacks)} exact covering inequalities ............... PASS")
    print(f"      minimum slack: {minimum_slack}")
    print(f"      minimum-slack index: q={minimum_index}")
    print(f"      equality indices: {equality_indices}")
    if least_positive is not None:
        print("      least positive slack: " + _display_fraction(least_positive, verbose))
    print("[5/7] Exact energy and boundary constants ............. PASS")
    print(f"      a = {_display_fraction(result.a, verbose)}")
    print(f"      b = {_display_fraction(result.b, verbose)}")
    print("      b > 0: yes")
    print("[6/7] Exact candidate bound ........................... PASS")
    print(f"      ab = {_display_fraction(result.ab, verbose)}")
    print(f"      ab < ({certificate.declared_bound})^2: yes")
    print(f"      gamma (decimal diagnostic): {candidate_gamma:.16f}")
    print("[7/7] Exact Hou-Zhao v2 comparison .................... PASS")
    print(f"      source: {HOU_ZHAO_ARXIV}")
    print(f"      Hou-Zhao ab = {_display_fraction(HOU_ZHAO_AB, verbose)}")
    print(f"      Hou-Zhao gamma (published display): {HOU_ZHAO_GAMMA_DISPLAY}")
    print("      candidate ab < Hou-Zhao ab: yes")
    print(
        "      exact squared-constant margin: "
        + _display_fraction(HOU_ZHAO_AB - result.ab, verbose)
    )
    print(f"      gamma improvement (decimal diagnostic): {gamma_improvement:.16f}")
    if verbose:
        print()
        print("All covering slacks")
        for index, slack in enumerate(result.slacks):
            print(f"  q={index:3d}: {slack}")
    print()
    print("=" * 54)
    if result.failures:
        print("EXACT VERIFICATION FAILED")
        for failure in result.failures:
            print(f"  - {failure}")
        return
    print("ALL EXACT CHECKS PASSED")
    print()
    print("Certified consequence under Hou-Zhao Lemma 2.1:")
    print("  F(N) <= N^(1/2)")
    print(f"          + {candidate_gamma:.16f}... N^(1/4)")
    print("          + O(1).")
    print()
    print("This improves the exact Hou-Zhao v2 certified coefficient.")
    print("It does not resolve Erdos Problem #30.")
    print("All proof-bearing calculations used exact rational arithmetic.")
    print("Decimals above are diagnostic displays only.")
    print("=" * 54)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("CERTIFICATE.json"),
        help="certificate path (default: CERTIFICATE.json beside this program)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print complete exact fractions and every covering slack",
    )
    args = parser.parse_args()
    try:
        certificate, digest = load_certificate(args.certificate)
        result = verify(certificate)
        print_report(
            args.certificate,
            digest,
            certificate,
            result,
            verbose=args.verbose,
        )
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError) as error:
        print("SIDON FRONTIER CERTIFICATE - EXACT VERIFICATION")
        print("=" * 54)
        print("EXACT VERIFICATION FAILED")
        print(f"  - {error}")
        return 1
    return 1 if result.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
