"""Independent exact replay of one-ramp, right-ones two-sided certificates.

Only the standard library is imported. No numerical producer, prefix operator,
shared mathematical checker or saved result is used. Positive integer m,L are
allowed for algebraic controls; the campaign runner owns its narrower grid
selection. A successful replay verifies a finite certificate, not the analytic
Sidon transfer theorem or optimality of the boundary.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

_FORMAT = "mathis.research.sidon.two_sided_smoothing_certificate.v1"
_FIELDS = frozenset(
    {
        "format_version",
        "block_size",
        "window_length",
        "declared_bound",
        "mixing",
        "kernels",
        "left_boundary",
        "right_boundary",
    }
)
_RATIONAL = re.compile(r"[+-]?[0-9]+(?:/[+-]?[0-9]+)?\Z")
_DEFAULT_COMPARATOR = Fraction(942809522, 10**9)


def _fraction(value: object, origin: str) -> Fraction:
    if not isinstance(value, str) or _RATIONAL.fullmatch(value) is None:
        raise ValueError(f"{origin}: expected an integer or rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{origin}: invalid rational") from error


def _object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _read(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise ValueError("certificate file could not be read") from error


def _parse(raw: bytes) -> tuple[int, int, tuple[Fraction, ...], tuple[Fraction, ...], Fraction]:
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
    except (ValueError, RecursionError) as error:
        raise ValueError(f"invalid certificate JSON: {error}") from error
    if not isinstance(data, dict) or set(data) != _FIELDS:
        raise ValueError("certificate must contain exactly the supported schema fields")
    if data["format_version"] != _FORMAT:
        raise ValueError("unsupported format_version")
    m, length = data["block_size"], data["window_length"]
    if type(m) is not int or m < 1:
        raise ValueError("block_size must be a positive integer")
    if type(length) is not int or length < 1:
        raise ValueError("window_length must be a positive integer")
    mixing = data["mixing"]
    if not isinstance(mixing, list) or len(mixing) != 1:
        raise ValueError("independent replay requires one mixing component")
    if _fraction(mixing[0], "mixing[0]") != 1:
        raise ValueError("independent replay requires mixing weight one")
    rows = data["kernels"]
    if (
        not isinstance(rows, list)
        or len(rows) != 1
        or not isinstance(rows[0], list)
        or len(rows[0]) != m
    ):
        raise ValueError("kernels must contain one row of block_size entries")
    kernel = tuple(_fraction(value, f"kernels[0][{i}]") for i, value in enumerate(rows[0]))
    if any(value != Fraction(2 * i + 1, m * m) for i, value in enumerate(kernel)):
        raise ValueError("independent replay requires the exact linear ramp kernel")
    boundaries = data["left_boundary"]
    if (
        not isinstance(boundaries, list)
        or len(boundaries) != 1
        or not isinstance(boundaries[0], list)
        or len(boundaries[0]) != m * length
    ):
        raise ValueError("left_boundary must contain one row of L*m entries")
    boundary = tuple(
        _fraction(value, f"left_boundary[0][{j}]") for j, value in enumerate(boundaries[0])
    )
    if data["right_boundary"] != "ones":
        raise ValueError("independent replay requires right_boundary='ones'")
    return m, length, kernel, boundary, _fraction(data["declared_bound"], "declared_bound")


def verify_certificate(
    path: str | Path, comparator: Fraction = _DEFAULT_COMPARATOR
) -> dict[str, object]:
    """Return deterministic exact acceptance data, or ValueError for malformed input.

    accepted_feasible includes every cover, positive a,b and declared bound,
    and strict ab<declared_bound**2. beats_target additionally requires a
    strictly smaller declaration than comparator. Rational results are canonical
    strings; covers/minslack describe both ends including the structural rows.
    The input bytes are read again before returning any result.
    """
    if (type(comparator) is not int and not isinstance(comparator, Fraction)) or comparator <= 0:
        raise ValueError("comparator must be a positive exact integer or Fraction")
    comparator = Fraction(comparator)
    try:
        source = Path(path)
    except (TypeError, ValueError) as error:
        raise ValueError("invalid certificate path") from error
    raw = _read(source)
    digest = hashlib.sha256(raw).hexdigest()
    m, length, kernel, boundary, declared = _parse(raw)
    n = m * length

    # Use direct original unscaled dots, deliberately without prefix operators.
    kernel_denominator = math.lcm(*(value.denominator for value in kernel))
    boundary_denominator = math.lcm(*(value.denominator for value in boundary))
    weights = [value.numerator * (kernel_denominator // value.denominator) for value in kernel]
    numerators = [
        value.numerator * (boundary_denominator // value.denominator) for value in boundary
    ]
    extended = numerators + [boundary_denominator] * m
    denominator = kernel_denominator * boundary_denominator
    failures = []
    left_minimum: Fraction | None = None
    for q in range(n + 1):
        covering = sum(weights[i] * extended[q + i] for i in range(m))
        slack = Fraction(covering - denominator, denominator)
        if left_minimum is None or slack < left_minimum:
            left_minimum = slack
        if slack < 0:
            failures.append(f"left covering inequality q={q} fails")

    # Reversed normalized kernel against an identically-one boundary and tail:
    # every original right dot, including q=n, is this same exact sum.
    right_covering = sum(reversed(kernel), Fraction(0))
    right_minimum = right_covering - 1
    if right_minimum != 0 or sum(kernel, Fraction(0)) != 1:
        raise ValueError("ramp normalization or right-one identity is inconsistent")
    a = m * sum((value * value for value in kernel), Fraction(0))
    b = 1 + sum((value * value - 1 for value in boundary), Fraction(0)) / m
    product = a * b
    if a <= 0:
        failures.append("kernel constant a is nonpositive")
    if b <= 0:
        failures.append("boundary constant b is nonpositive")
    if declared <= 0:
        failures.append("declared_bound is nonpositive")
    strict_bound = a > 0 and b > 0 and declared > 0 and product < declared * declared
    if not strict_bound:
        failures.append("strict coefficient bound fails")
    stable = _read(source)
    if hashlib.sha256(stable).hexdigest() != digest or stable != raw:
        raise ValueError("certificate input changed during independent replay")
    if left_minimum is None:
        raise ValueError("no covering rows were reconstructed")
    accepted = not failures
    return {
        "accepted_feasible": accepted,
        "beats_target": accepted and declared < comparator,
        "a": str(a),
        "b": str(b),
        "ab": str(product),
        "declared_bound": str(declared),
        "comparator": str(comparator),
        "sha256": digest,
        "block_size": m,
        "window_length": length,
        "covers": {"left": n + 1, "right": n + 1, "total": 2 * (n + 1)},
        "minslack": {
            "left": str(left_minimum),
            "right": str(right_minimum),
            "overall": str(min(left_minimum, right_minimum)),
        },
        "failures": failures,
        "input_unchanged": True,
    }
