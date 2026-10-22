"""Exact verifier for vector-valued smoothing certificates (Gate S2).

The module re-derives, from first principles and exact rational arithmetic
only, the finite conditions of the vector smoothing lemma of Hou and Zhao,
``Vector-valued smoothing for finite Sidon sets`` (arXiv:2607.01169v2):

* kernels are symmetric probability vectors ``p^(r)`` of length ``m``;
* mixing weights satisfy ``lambda_r >= 0`` and sum to one;
* boundary weights ``w^(r)_j`` are declared for ``j < L*m`` and extended by
  the constant one;
* the ``L*m + 1`` covering inequalities must hold;
* ``a = m * sum_r lambda_r * sum_i p_i^(r)^2`` and
  ``b = 1 + 2 * ((1/m) * sum_r lambda_r * sum_j w_j^(r)^2 - L)`` must satisfy
  ``b > 0`` and ``a*b < declared_bound^2``.

A uniform single-kernel certificate reproduces the classical Erdos-Turan
coefficient exactly and serves as the built-in calibration control.  The
numerical search that produces candidate certificates is out of scope here
and is never trusted.  Research instrumentation only.
"""

from __future__ import annotations

import ast
import json
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

CERTIFICATE_SCHEMA = "mathis.research.sidon.smoothing_certificate.v1"
TWO_SIDED_CERTIFICATE_SCHEMA = "mathis.research.sidon.two_sided_smoothing_certificate.v1"
CALIBRATION_BOUND = Fraction(1, 1)


class NonpositiveDeclaredBoundError(ValueError):
    """A rational coefficient declaration fails the positive-bound condition."""


def _check_dimensions(block_size: object, window_length: object) -> None:
    if type(block_size) is not int or block_size < 1:
        raise ValueError("block_size must be a positive integer")
    if type(window_length) is not int or window_length < 1:
        raise ValueError("window_length must be a positive integer")


def _check_exact_number(value: object, origin: str) -> None:
    if type(value) is not int and not isinstance(value, Fraction):
        raise TypeError(f"{origin}: expected an exact integer or Fraction")


def _check_typed_shapes(
    mixing: tuple[Fraction, ...],
    kernels: tuple[tuple[Fraction, ...], ...],
    boundary_groups: tuple[tuple[tuple[Fraction, ...], ...], ...],
    block_size: int,
    window_length: int,
    declared_bound: Fraction,
) -> None:
    """Validate direct API inputs as well as documents parsed from JSON."""
    _check_dimensions(block_size, window_length)
    _check_exact_number(declared_bound, "declared_bound")
    if not isinstance(mixing, tuple | list) or not mixing:
        raise ValueError("mixing must be a nonempty sequence")
    for index, value in enumerate(mixing):
        _check_exact_number(value, f"mixing[{index}]")
    for name, rows, expected_length in (
        ("kernels", kernels, block_size),
        *(("boundary", group, block_size * window_length) for group in boundary_groups),
    ):
        if not isinstance(rows, tuple | list) or len(rows) != len(mixing):
            raise ValueError(f"{name} component count must match mixing")
        for r, row in enumerate(rows):
            if not isinstance(row, tuple | list) or len(row) != expected_length:
                raise ValueError(f"{name}[{r}] must contain {expected_length} entries")
            for j, value in enumerate(row):
                _check_exact_number(value, f"{name}[{r}][{j}]")


def fraction_from_text(raw: object, origin: str) -> Fraction:
    """Parse one strict rational string of the form ``p/q`` or plain ``p``."""

    if isinstance(raw, str) and "/" in raw:
        numerator, denominator = raw.split("/", 1)
        if int(denominator) == 0:
            raise ValueError(f"{origin}: zero denominator")
        return Fraction(int(numerator), int(denominator))
    if isinstance(raw, str) and raw.lstrip("-").isdigit():
        return Fraction(int(raw))
    raise ValueError(f"{origin}: expected a rational string numerator/denominator")


@dataclass(frozen=True, slots=True)
class SmoothingCertificate:
    """One exact rational smoothing certificate."""

    mixing: tuple[Fraction, ...]
    kernels: tuple[tuple[Fraction, ...], ...]
    boundary: tuple[tuple[Fraction, ...], ...]
    window_length: int
    block_size: int
    declared_bound: Fraction

    @property
    def kernel_count(self) -> int:
        return len(self.mixing)

    @property
    def covering_count(self) -> int:
        return self.window_length * self.block_size + 1


def _weight(
    certificate: SmoothingCertificate,
    kernel: int,
    index: int,
) -> Fraction:
    if index < len(certificate.boundary[kernel]):
        return certificate.boundary[kernel][index]
    return Fraction(1, 1)


def build_uniform_certificate(
    *,
    block_size: int = 4,
    window_length: int = 2,
) -> SmoothingCertificate:
    """Build the uniform single-kernel calibration certificate.

    The uniform kernel has ``a = 1``, and constant boundary weights give
    ``b = 1``; hence the certified coefficient is exactly ``1``, recovering
    the classical Erdos-Turan secondary term as a calibration control.
    """

    count = window_length * block_size
    return SmoothingCertificate(
        mixing=(Fraction(1, 1),),
        kernels=(tuple(Fraction(1, block_size) for _ in range(block_size)),),
        boundary=(tuple(Fraction(1, 1) for _ in range(count)),),
        window_length=window_length,
        block_size=block_size,
        declared_bound=CALIBRATION_BOUND,
    )


def parse_certificate(payload: Mapping[str, object]) -> SmoothingCertificate:
    """Parse one strict certificate document."""

    version = payload.get("format_version")
    if version != CERTIFICATE_SCHEMA:
        raise ValueError("format_version must be " + CERTIFICATE_SCHEMA)
    unknown = set(payload) - {
        "format_version",
        "block_size",
        "window_length",
        "declared_bound",
        "mixing",
        "kernels",
        "boundary",
    }
    if unknown:
        raise ValueError(f"unknown certificate fields {sorted(unknown)}")

    block_size = payload["block_size"]
    window_length = payload["window_length"]
    _check_dimensions(block_size, window_length)
    declared_bound = fraction_from_text(payload.get("declared_bound"), "declared_bound")
    if declared_bound <= 0:
        raise NonpositiveDeclaredBoundError("declared_bound must be positive")

    mixing_raw = payload.get("mixing")
    kernels_raw = payload.get("kernels")
    boundary_raw = payload.get("boundary")
    for name, value in (
        ("mixing", mixing_raw),
        ("kernels", kernels_raw),
        ("boundary", boundary_raw),
    ):
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a list")
    for name, rows in (("kernels", kernels_raw), ("boundary", boundary_raw)):
        if any(not isinstance(row, list) for row in rows):
            raise TypeError(f"{name} rows must be lists")
    if not mixing_raw:
        raise ValueError("mixing must be nonempty")
    mixing = tuple(
        fraction_from_text(item, f"mixing[{index}]") for index, item in enumerate(mixing_raw)
    )
    kernels = tuple(
        tuple(fraction_from_text(item, f"kernels[{r}][{i}]") for i, item in enumerate(row))
        for r, row in enumerate(kernels_raw)
    )
    boundary = tuple(
        tuple(fraction_from_text(item, f"boundary[{r}][{j}]") for j, item in enumerate(row))
        for r, row in enumerate(boundary_raw)
    )
    if len(kernels) != len(mixing) or len(boundary) != len(mixing):
        raise ValueError("mixing, kernels, and boundary counts must agree")
    expected_boundary = window_length * block_size
    for r, row in enumerate(boundary):
        if len(row) != expected_boundary:
            raise ValueError(f"boundary[{r}] must contain {expected_boundary} entries")
    for r, row in enumerate(kernels):
        if len(row) != block_size:
            raise ValueError(f"kernels[{r}] must contain {block_size} entries")
    return SmoothingCertificate(
        mixing=mixing,
        kernels=kernels,
        boundary=boundary,
        window_length=window_length,
        block_size=block_size,
        declared_bound=declared_bound,
    )


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """Outcome of one exact certificate verification."""

    checks_passed: bool
    failures: tuple[str, ...]
    energy_constant: Fraction
    boundary_constant: Fraction
    gamma_squared: Fraction
    declared_bound: Fraction
    minimum_slack_index: int | None
    minimum_slack: Fraction | None
    bound_holds: bool

    @property
    def gamma_decimal_diagnostic(self) -> float | None:
        """Display only; invalid or unrepresentable products have no real diagnostic."""
        if self.gamma_squared < 0:
            return None
        try:
            value = float(self.gamma_squared)
        except OverflowError:
            return None
        return math.sqrt(value) if math.isfinite(value) else None

    def to_dict(self) -> dict[str, object]:
        return {
            "checks_passed": self.checks_passed,
            "failures": list(self.failures),
            "energy_constant_a": str(self.energy_constant),
            "boundary_constant_b": str(self.boundary_constant),
            "gamma_squared_ab": str(self.gamma_squared),
            "gamma_float_diagnostic_only": self.gamma_decimal_diagnostic,
            "minimum_covering_slack_index": self.minimum_slack_index,
            "minimum_covering_slack": None
            if self.minimum_slack is None
            else str(self.minimum_slack),
            "declared_bound": str(self.declared_bound),
            "bound_strictly_holds": self.bound_holds,
        }


def verify_certificate(certificate: SmoothingCertificate) -> VerificationResult:
    """Run every exact lemma condition on one certificate."""

    failures: list[str] = []
    _check_typed_shapes(
        certificate.mixing,
        certificate.kernels,
        (certificate.boundary,),
        certificate.block_size,
        certificate.window_length,
        certificate.declared_bound,
    )
    if certificate.declared_bound <= 0:
        failures.append("declared_bound must be positive")
    m = certificate.block_size
    n = certificate.window_length * m

    total_mixing = sum(certificate.mixing, Fraction(0, 1))
    if any(weight < 0 for weight in certificate.mixing):
        failures.append("negative mixing weight")
    if total_mixing != 1:
        failures.append("mixing weights do not sum to one")

    for r, kernel in enumerate(certificate.kernels):
        if any(value < 0 for value in kernel):
            failures.append(f"kernel {r} has a negative probability")
        if sum(kernel, Fraction(0, 1)) != 1:
            failures.append(f"kernel {r} does not sum to one")
        if any(kernel[i] != kernel[m - 1 - i] for i in range(m)):
            failures.append(f"kernel {r} is not symmetric")

    slacks: list[Fraction] = []
    for q in range(n + 1):
        covered = Fraction(0, 1)
        for r in range(certificate.kernel_count):
            for i in range(m):
                covered += (
                    certificate.mixing[r]
                    * certificate.kernels[r][i]
                    * _weight(certificate, r, q + i)
                )
        if covered < 1:
            failures.append(f"covering inequality q={q} fails with mass {covered}")
        slacks.append(covered - 1)

    energy = Fraction(0, 1)
    boundary_energy = Fraction(0, 1)
    for r in range(certificate.kernel_count):
        energy += certificate.mixing[r] * sum(
            (value * value for value in certificate.kernels[r]),
            Fraction(0, 1),
        )
        boundary_energy += certificate.mixing[r] * sum(
            (value * value for value in certificate.boundary[r]),
            Fraction(0, 1),
        )
    a = m * energy
    b = 1 + 2 * (boundary_energy / m - certificate.window_length)
    if b <= 0:
        failures.append("boundary constant b is nonpositive")
    gamma_squared = a * b
    minimum_index = None
    minimum_value = None
    if slacks:
        minimum_value = min(slacks)
        minimum_index = slacks.index(minimum_value)
    bound_holds = (
        certificate.declared_bound > 0
        and a > 0
        and b > 0
        and gamma_squared < certificate.declared_bound**2
    )
    if not bound_holds:
        failures.append("ab does not fall strictly below the declared bound squared")
    return VerificationResult(
        checks_passed=not failures,
        failures=tuple(failures),
        energy_constant=a,
        boundary_constant=b,
        gamma_squared=gamma_squared,
        declared_bound=certificate.declared_bound,
        minimum_slack_index=minimum_index,
        minimum_slack=minimum_value,
        bound_holds=bound_holds,
    )


@dataclass(frozen=True, slots=True)
class TwoSidedSmoothingCertificate:
    """One exact rational two-sided smoothing certificate (Proposition 2.3)."""

    mixing: tuple[Fraction, ...]
    kernels: tuple[tuple[Fraction, ...], ...]
    left_boundary: tuple[tuple[Fraction, ...], ...]
    right_boundary: tuple[tuple[Fraction, ...], ...]
    window_length: int
    block_size: int
    declared_bound: Fraction

    @property
    def kernel_count(self) -> int:
        return len(self.mixing)

    @property
    def covering_count(self) -> int:
        return self.window_length * self.block_size + 1


def parse_two_sided_certificate(payload: Mapping[str, object]) -> TwoSidedSmoothingCertificate:
    """Parse one strict two-sided smoothing certificate document."""

    version = payload.get("format_version")
    if version != TWO_SIDED_CERTIFICATE_SCHEMA:
        raise ValueError("format_version must be " + TWO_SIDED_CERTIFICATE_SCHEMA)
    unknown = set(payload) - {
        "format_version",
        "block_size",
        "window_length",
        "declared_bound",
        "mixing",
        "kernels",
        "left_boundary",
        "right_boundary",
    }
    if unknown:
        raise ValueError(f"unknown certificate fields {sorted(unknown)}")

    block_size = payload.get("block_size")
    window_length = payload.get("window_length")
    _check_dimensions(block_size, window_length)
    declared_bound = fraction_from_text(payload.get("declared_bound"), "declared_bound")
    if declared_bound <= 0:
        raise NonpositiveDeclaredBoundError("declared_bound must be positive")

    mixing_raw = payload.get("mixing")
    kernels_raw = payload.get("kernels")
    left_raw = payload.get("left_boundary")
    right_raw = payload.get("right_boundary")

    for name, value in (
        ("mixing", mixing_raw),
        ("kernels", kernels_raw),
        ("left_boundary", left_raw),
    ):
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a list")
    for name, rows in (("kernels", kernels_raw), ("left_boundary", left_raw)):
        if any(not isinstance(row, list) for row in rows):
            raise TypeError(f"{name} rows must be lists")
    if not mixing_raw:
        raise ValueError("mixing must be nonempty")

    mixing = tuple(
        fraction_from_text(item, f"mixing[{index}]") for index, item in enumerate(mixing_raw)
    )
    kernels = tuple(
        tuple(fraction_from_text(item, f"kernels[{r}][{i}]") for i, item in enumerate(row))
        for r, row in enumerate(kernels_raw)
    )
    left_boundary = tuple(
        tuple(fraction_from_text(item, f"left_boundary[{r}][{j}]") for j, item in enumerate(row))
        for r, row in enumerate(left_raw)
    )
    expected_boundary = window_length * block_size
    if right_raw == "ones":
        right_boundary = tuple(
            tuple(Fraction(1, 1) for _ in range(expected_boundary)) for _ in range(len(mixing))
        )
    elif isinstance(right_raw, list):
        if any(not isinstance(row, list) for row in right_raw):
            raise TypeError("right_boundary rows must be lists")
        right_boundary = tuple(
            tuple(
                fraction_from_text(item, f"right_boundary[{r}][{j}]") for j, item in enumerate(row)
            )
            for r, row in enumerate(right_raw)
        )
    else:
        raise TypeError("right_boundary must be a list or 'ones'")

    if (
        len(kernels) != len(mixing)
        or len(left_boundary) != len(mixing)
        or len(right_boundary) != len(mixing)
    ):
        raise ValueError("mixing, kernels, left_boundary, and right_boundary counts must agree")
    for r, row in enumerate(left_boundary):
        if len(row) != expected_boundary:
            raise ValueError(f"left_boundary[{r}] must contain {expected_boundary} entries")
    for r, row in enumerate(right_boundary):
        if len(row) != expected_boundary:
            raise ValueError(f"right_boundary[{r}] must contain {expected_boundary} entries")
    for r, row in enumerate(kernels):
        if len(row) != block_size:
            raise ValueError(f"kernels[{r}] must contain {block_size} entries")

    return TwoSidedSmoothingCertificate(
        mixing=mixing,
        kernels=kernels,
        left_boundary=left_boundary,
        right_boundary=right_boundary,
        window_length=window_length,
        block_size=block_size,
        declared_bound=declared_bound,
    )


def _exact_covering_sums(
    kernel: tuple[Fraction, ...],
    boundary: tuple[Fraction, ...],
    m: int,
    n: int,
) -> list[Fraction]:
    """Compute exact kernel/boundary dot products for all rows q=0..n, including the tail."""
    dp = math.lcm(*(x.denominator for x in kernel)) if kernel else 1
    du = math.lcm(*(x.denominator for x in boundary)) if boundary else 1
    p_ints = [x.numerator * (dp // x.denominator) for x in kernel]
    u_ints = [x.numerator * (du // x.denominator) for x in boundary] + [du] * m
    denom = dp * du
    out: list[Fraction] = []
    for q in range(n + 1):
        dot = sum(p_ints[i] * u_ints[q + i] for i in range(m))
        out.append(Fraction(dot, denom))
    return out


def verify_two_sided_certificate(
    certificate: TwoSidedSmoothingCertificate,
) -> VerificationResult:
    """Run every exact lemma condition of Proposition 2.3 on a two-sided smoothing certificate."""

    failures: list[str] = []
    _check_typed_shapes(
        certificate.mixing,
        certificate.kernels,
        (certificate.left_boundary, certificate.right_boundary),
        certificate.block_size,
        certificate.window_length,
        certificate.declared_bound,
    )
    if certificate.declared_bound <= 0:
        failures.append("declared_bound must be positive")
    m = certificate.block_size
    n = certificate.window_length * m

    total_mixing = sum(certificate.mixing, Fraction(0, 1))
    if any(weight < 0 for weight in certificate.mixing):
        failures.append("negative mixing weight")
    if total_mixing != 1:
        failures.append("mixing weights do not sum to one")

    for r, kernel in enumerate(certificate.kernels):
        if any(value < 0 for value in kernel):
            failures.append(f"kernel {r} has a negative probability")
        if sum(kernel, Fraction(0, 1)) != 1:
            failures.append(f"kernel {r} does not sum to one")

    left_sums_by_r = [
        _exact_covering_sums(certificate.kernels[r], certificate.left_boundary[r], m, n)
        for r in range(certificate.kernel_count)
    ]
    right_sums_by_r = [
        _exact_covering_sums(
            tuple(reversed(certificate.kernels[r])),
            certificate.right_boundary[r],
            m,
            n,
        )
        for r in range(certificate.kernel_count)
    ]

    slacks: list[Fraction] = []
    for q in range(n + 1):
        cov_left = sum(
            (certificate.mixing[r] * left_sums_by_r[r][q] for r in range(certificate.kernel_count)),
            Fraction(0, 1),
        )
        if cov_left < 1:
            failures.append(f"left covering inequality q={q} fails with mass {cov_left}")
        slacks.append(cov_left - 1)

    for q in range(n + 1):
        cov_right = sum(
            (
                certificate.mixing[r] * right_sums_by_r[r][q]
                for r in range(certificate.kernel_count)
            ),
            Fraction(0, 1),
        )
        if cov_right < 1:
            failures.append(f"right covering inequality q={q} fails with mass {cov_right}")
        slacks.append(cov_right - 1)

    energy = Fraction(0, 1)
    boundary_energy = Fraction(0, 1)
    for r in range(certificate.kernel_count):
        energy += certificate.mixing[r] * sum(
            (value * value for value in certificate.kernels[r]),
            Fraction(0, 1),
        )
        left_sq = sum(
            (value * value for value in certificate.left_boundary[r]),
            Fraction(0, 1),
        )
        right_sq = sum(
            (value * value for value in certificate.right_boundary[r]),
            Fraction(0, 1),
        )
        boundary_energy += certificate.mixing[r] * (left_sq + right_sq)

    a = m * energy
    b = 1 + (boundary_energy / m - 2 * certificate.window_length)
    if b <= 0:
        failures.append("boundary constant b is nonpositive")
    gamma_squared = a * b
    minimum_index = None
    minimum_value = None
    if slacks:
        minimum_value = min(slacks)
        minimum_index = slacks.index(minimum_value)
    bound_holds = (
        certificate.declared_bound > 0
        and a > 0
        and b > 0
        and gamma_squared < certificate.declared_bound**2
    )
    if not bound_holds:
        failures.append("ab does not fall strictly below the declared bound squared")
    return VerificationResult(
        checks_passed=not failures,
        failures=tuple(failures),
        energy_constant=a,
        boundary_constant=b,
        gamma_squared=gamma_squared,
        declared_bound=certificate.declared_bound,
        minimum_slack_index=minimum_index,
        minimum_slack=minimum_value,
        bound_holds=bound_holds,
    )


def write_two_sided_certificate(
    certificate: TwoSidedSmoothingCertificate,
    path: Path,
    *,
    compact_ones_right: bool = True,
) -> None:
    """Serialize one two-sided smoothing certificate deterministically."""
    all_ones_right = compact_ones_right and all(
        all(val == 1 for val in row) for row in certificate.right_boundary
    )
    document = {
        "format_version": TWO_SIDED_CERTIFICATE_SCHEMA,
        "block_size": certificate.block_size,
        "window_length": certificate.window_length,
        "declared_bound": str(certificate.declared_bound),
        "mixing": [str(weight) for weight in certificate.mixing],
        "kernels": [[str(value) for value in kernel] for kernel in certificate.kernels],
        "left_boundary": [[str(value) for value in row] for row in certificate.left_boundary],
        "right_boundary": "ones"
        if all_ones_right
        else [[str(value) for value in row] for row in certificate.right_boundary],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_and_verify(path: Path, *, mode: str = "auto") -> VerificationResult:
    """Load one certificate document and verify it exactly in symmetric or two-sided mode."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("certificate document must be a JSON object")
    if mode not in ("auto", "symmetric", "two-sided"):
        raise ValueError("mode must be 'auto', 'symmetric', or 'two-sided'")
    version = payload.get("format_version")
    if mode == "two-sided" or (mode == "auto" and version == TWO_SIDED_CERTIFICATE_SCHEMA):
        return verify_two_sided_certificate(parse_two_sided_certificate(payload))
    return verify_certificate(parse_certificate(payload))


PUBLISHED_VERIFIER_SHA256 = "957a5afadd849ac4f97c2b71252abb5c796c2db3c91a608ab35097e3c49292a8"
ZHAO_EXPECTED_A = Fraction(
    497329054138522113993707809619,
    390625000000000000000000000000,
)
ZHAO_EXPECTED_B = Fraction(
    69918675237166718360455326217,
    100000000000000000000000000000,
)


def _source_literals(source: str) -> dict[str, object]:
    """Extract top-level literal assignments from producer source safely.

    Only ``ast.literal_eval`` is applied to right-hand sides; producer code
    is never executed.
    """

    tree = ast.parse(source)
    values: dict[str, object] = {}
    pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        if not pattern.match(name):
            continue
        try:
            values[name] = ast.literal_eval(node.value)
        except ValueError:
            continue
    return values


def parse_zhao_source_certificate(path: Path) -> tuple[SmoothingCertificate, dict[str, object]]:
    """Convert the published eight-kernel source into our strict schema.

    The source stores symmetric kernels as mirrored half-vectors over a
    common denominator and boundary weights with an additive rational
    correction already applied by the published verifier.  Conversion is
    purely structural; every mathematical condition is re-checked here.
    """

    source = path.read_text(encoding="utf-8")
    literals = _source_literals(source)
    required = {
        "R",
        "m",
        "L",
        "DL",
        "DP",
        "DQ",
        "LAMBDA_INTS",
        "W1_INTS",
        "W2_INTS",
        "W3_INTS",
        "W4_INTS",
        "W5_INTS",
        "W6_INTS",
        "W7_INTS",
        "W8_INTS",
    }
    missing = {name for name in required if name not in literals}
    if missing:
        raise ValueError(f"producer source is missing assignments {sorted(missing)}")
    r_count = int(literals["R"])
    m = int(literals["m"])
    window_length = int(literals["L"])
    dl = int(literals["DL"])
    dp = int(literals["DP"])
    dq = int(literals["DQ"])
    eta_match = re.search(r"ETA\s*=\s*F\((\d+),\s*(\d+)\)", source)
    if eta_match is None:
        raise ValueError("producer source does not declare ETA as a rational")
    eta = Fraction(int(eta_match.group(1)), int(eta_match.group(2)))

    mixing_values = literals["LAMBDA_INTS"]
    if not isinstance(mixing_values, list) or len(mixing_values) != r_count:
        raise ValueError("unexpected mixing weight list")
    mixing = tuple(Fraction(int(x), dl) for x in mixing_values)

    uniform_index = 2
    kernels: list[tuple[Fraction, ...]] = []
    for index in range(1, r_count + 1):
        if index == uniform_index:
            kernels.append(tuple(Fraction(1, m) for _ in range(m)))
            continue
        half_key = f"P{index}_HALF_INTS"
        half = literals.get(half_key)
        if not isinstance(half, list) or len(half) * 2 != m:
            raise ValueError(f"unexpected kernel half-vector {half_key}")
        full = [Fraction(int(x), dp) for x in half]
        kernels.append(tuple(full + list(reversed(full))))

    boundary: list[tuple[Fraction, ...]] = []
    for index in range(1, r_count + 1):
        row = literals[f"W{index}_INTS"]
        if not isinstance(row, list) or len(row) != window_length * m:
            raise ValueError(f"unexpected boundary vector W{index}_INTS")
        boundary.append(tuple(Fraction(int(x), dq) + eta for x in row))

    certificate = SmoothingCertificate(
        mixing=mixing,
        kernels=tuple(kernels),
        boundary=tuple(boundary),
        window_length=window_length,
        block_size=m,
        declared_bound=Fraction(9435, 10000),
    )
    provenance = {
        "source_file": str(path),
        "published_verifier_sha256": PUBLISHED_VERIFIER_SHA256,
        "expected_a_from_paper": str(ZHAO_EXPECTED_A),
        "expected_b_from_paper": str(ZHAO_EXPECTED_B),
        "eta_correction": str(eta),
    }
    return certificate, provenance


def write_certificate(certificate: SmoothingCertificate, path: Path) -> None:
    """Serialize one certificate deterministically."""

    document = {
        "format_version": CERTIFICATE_SCHEMA,
        "block_size": certificate.block_size,
        "window_length": certificate.window_length,
        "declared_bound": str(certificate.declared_bound),
        "mixing": [str(weight) for weight in certificate.mixing],
        "kernels": [[str(value) for value in kernel] for kernel in certificate.kernels],
        "boundary": [[str(value) for value in row] for row in certificate.boundary],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
