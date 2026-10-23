"""Independent compact renewal replay; Python 3.10+, standard library only.

No producer arithmetic is imported. Resume states are private checkpoints whose
bytes must be authenticated by the caller before use; input identity is checked
again here. Published states and supplied states never alias live accumulators.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

FORMAT = "mathis.public.sidon.renewal_certificate.v1"
STATE_FORMAT = "mathis.public.sidon.renewal_replay_state.v1"
INTEGER_CAP = 131_072
ENTRY_CAP = 4096
FIELDS = {
    "format_version",
    "n",
    "L",
    "s",
    "p",
    "target",
    "coarse_y_hex",
    "full_hex",
    "full_den_hex",
    "V",
    "a",
    "b",
    "ab",
    "lower_sha256",
    "upper_sha256",
    "source_bindings",
}

SOURCE_FIELDS = {
    "research_core_sha256",
    "research_derivation_sha256",
    "research_dense_gzip_sha256",
}


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def _read(path: Path) -> tuple[dict, str]:
    if path.stat().st_size > 256 * (1 << 20):
        raise ValueError("compact witness exceeds verifier input envelope")
    raw = path.read_bytes()
    data = json.loads(
        raw,
        object_pairs_hook=_unique_object,
        parse_constant=_forbidden,
        parse_float=_forbidden,
    )
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    return data, hashlib.sha256(raw).hexdigest()


def _forbidden(value: str) -> None:
    raise ValueError("inexact JSON number is forbidden: " + value)


def _digest(value: object) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise ValueError("expected a lowercase SHA-256 digest")
    return value


def _integer(value: object) -> int:
    if not isinstance(value, str) or not value or len(value) > INTEGER_CAP // 4 + 2:
        raise ValueError("invalid hexadecimal integer")
    try:
        result = int(value, 16)
    except ValueError as exc:
        raise ValueError("invalid hexadecimal integer") from exc
    if format(result, "x") != value or abs(result).bit_length() > INTEGER_CAP:
        raise ValueError("noncanonical or oversized hexadecimal integer")
    return result


def _integers(value: object, length: int) -> list[int]:
    if not isinstance(value, list) or len(value) != length:
        raise ValueError("integer vector has the wrong geometry")
    return [_integer(x) for x in value]


def _rational(value: object) -> Fraction:
    if not isinstance(value, str):
        raise ValueError("expected a reduced rational string")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational string") from exc
    if str(result) != value:
        raise ValueError("noncanonical rational string")
    if max(abs(result.numerator).bit_length(), result.denominator.bit_length()) > INTEGER_CAP:
        raise ValueError("rational exceeds arithmetic cap")
    return result


def _geometry(data: dict) -> tuple[int, int, int, int]:
    values = tuple(data.get(key) for key in ("n", "L", "s", "p"))
    if any(type(x) is not int for x in values):
        raise ValueError("geometry and fractional bits must be integers")
    n, depth, bits, proposal_bits = values
    if not (1 <= n <= 2048 and 1 <= depth <= 32 and 1 <= proposal_bits <= bits <= 256):
        raise ValueError("geometry exceeds the public verification envelope")
    return n, depth, bits, proposal_bits


def _nearest_even(numerator: int, denominator: int) -> int:
    quotient, remainder = divmod(numerator, denominator)
    doubled = 2 * remainder
    return quotient + (doubled > denominator or (doubled == denominator and quotient % 2))


def _renewal(
    n: int, depth: int, bits: int, proposal_bits: int, guard: Callable[[], None]
) -> tuple[list[int], str, str]:
    """Indexed interval replay; prefix arrays replace the producer's ring."""
    count, divisor, unit = n * depth, 2 * n - 1, 1 << bits
    low = [n * n * unit // divisor]
    high = [-((-n * n * unit) // divisor)]
    low_prefix, high_prefix = [0, low[0]], [0, high[0]]
    lower_hash, upper_hash = hashlib.sha256(), hashlib.sha256()
    rounded = []
    rounding_divisor = 1 << (bits - proposal_bits + 1)
    for t in range(count):
        if t % 1024 == 0:
            guard()
        if t:
            start = max(0, t - n + 1)
            left = 2 * (low_prefix[t] - low_prefix[start])
            right = 2 * (high_prefix[t] - high_prefix[start])
            if t >= n:
                left += low[t - n]
                right += high[t - n]
            low.append(left // divisor)
            high.append(-((-right) // divisor))
            low_prefix.append(low_prefix[-1] + low[-1])
            high_prefix.append(high_prefix[-1] + high[-1])
        lower_hash.update((format(low[t], "x") + "\n").encode())
        upper_hash.update((format(high[t], "x") + "\n").encode())
        rounded.append(_nearest_even(low[t] + high[t], rounding_divisor))
    return rounded, lower_hash.hexdigest(), upper_hash.hexdigest()


def _residue_prefix(values: list[int], width: int) -> list[int]:
    """Causal geometric sum, formed before the two shifted endpoints."""
    result = values.copy()
    for j in range(width, len(result)):
        result[j] += result[j - width]
    return result


def _residue_suffix(values: list[int], width: int) -> list[int]:
    result = values.copy()
    for j in range(len(result) - width - 1, -1, -1):
        result[j] += result[j + width]
    return result


def _past_endpoints(prefix: list[int], n: int, k: int) -> list[int]:
    shift = n - k
    return [
        (prefix[j - shift] if j >= shift else 0)
        - (prefix[j - shift - 2 * k] if j >= shift + 2 * k else 0)
        for j in range(len(prefix))
    ]


def _future_endpoints(suffix: list[int], n: int, k: int) -> list[int]:
    shift, size = n - k, len(suffix)
    return [
        (suffix[j + shift] if j + shift < size else 0)
        - (suffix[j + shift + 2 * k] if j + shift + 2 * k < size else 0)
        for j in range(size)
    ]


def _widest_core(coarse: list[int], n: int) -> list[int]:
    prefix = [0]
    for value in coarse:
        prefix.append(prefix[-1] + value)
    result = []
    for t in range(len(coarse)):
        value = prefix[t + 1] - prefix[max(0, t - n + 1)]
        result.extend((value, value))
    return result


def _entry_cap(values: list[int], denominator: int) -> None:
    for value in values:
        common = math.gcd(value, denominator)
        if max(abs(value // common).bit_length(), (denominator // common).bit_length()) > ENTRY_CAP:
            raise ValueError("original rational entry exceeds the 4096-bit cap")


def _hex_state(binding: str, next_k: int, flat: list[int], wu: list[int], energy: int) -> dict:
    return {
        "format_version": STATE_FORMAT,
        "binding": binding,
        "next_k": next_k,
        "flat_hex": [format(x, "x") for x in flat],
        "wu_hex": [format(x, "x") for x in wu],
        "energy_hex": format(energy, "x"),
    }


def verify(
    path: str | Path,
    *,
    state: dict | None = None,
    progress: Callable[[dict], None] = lambda _: None,
    guard: Callable[[], None] = lambda: None,
) -> dict:
    """Verify original covers, energy, recurrence and a strict target bound.

    The finite residual is computed after invertible widest-box
    preconditioning. It checks every original cover, rather than assuming
    that the producer's repair or reported energies were computed correctly.
    """
    artifact = Path(path)
    data, binding = _read(artifact)
    if set(data) != FIELDS or data.get("format_version") != FORMAT:
        raise ValueError("wrong public renewal witness schema")
    n, depth, bits, proposal_bits = _geometry(data)
    size, scale, d = 2 * n * depth, 1 << proposal_bits, 2 * n - 1
    target = _rational(data["target"])
    if target <= 0:
        raise ValueError("target must be positive")
    bindings = data["source_bindings"]
    if not isinstance(bindings, dict) or set(bindings) != SOURCE_FIELDS:
        raise ValueError("invalid source provenance bindings")
    for value in bindings.values():
        _digest(value)

    supplied_coarse = _integers(data["coarse_y_hex"], n * depth)
    coarse, lower_digest, upper_digest = _renewal(n, depth, bits, proposal_bits, guard)
    if supplied_coarse != coarse:
        raise ValueError("coarse proposal differs from independent directed recurrence")
    if (
        _digest(data["lower_sha256"]) != lower_digest
        or _digest(data["upper_sha256"]) != upper_digest
    ):
        raise ValueError("independently replayed interval endpoint hash mismatch")

    full = _integers(data["full_hex"], size)
    full_denominator = _integer(data["full_den_hex"])
    if full_denominator != n * d * scale:
        raise ValueError("wrong widest-component denominator")
    _entry_cap(full, full_denominator)
    # Nk is also a k-term causal sum of the independently authenticated q.
    # This proves the entry cap for every implicit nonfull original entry.
    if max((n * max(coarse)).bit_length(), (n * scale).bit_length()) > ENTRY_CAP:
        raise ValueError("implicit original entries exceed the 4096-bit cap")

    u = _widest_core(coarse, n)
    past = _residue_prefix(u, 2 * n)
    future_ones = _residue_suffix([1] * size, 2 * n)
    if state is None:
        next_k = 1
        flat, wu = [d * n] * size, [d * value for value in u]
        energy = 0
    else:
        private = copy.deepcopy(state)
        if (
            private.get("format_version") != STATE_FORMAT
            or private.get("binding") != binding
            or type(private.get("next_k")) is not int
            or not 1 <= private["next_k"] <= n
        ):
            raise ValueError("core verifier checkpoint identity or cursor mismatch")
        next_k = private["next_k"]
        flat = _integers(private.get("flat_hex"), size)
        wu = _integers(private.get("wu_hex"), size)
        energy = _integer(private.get("energy_hex"))
        if energy < 0:
            raise ValueError("negative checkpoint energy")

    for k in range(next_k, n):
        guard()
        nk = _past_endpoints(past, n, k)
        if any(nk[: n - k]):
            raise ValueError("implicit original invisible prefix is nonzero")
        aa = _future_endpoints(_residue_suffix(nk, 2 * n), n, k)
        a_one = _future_endpoints(future_ones, n, k)
        coefficient = 4 * k
        energy += coefficient * sum(value * value for value in nk)
        for j in range(size):
            flat[j] += coefficient * k * a_one[j]
            wu[j] += coefficient * aa[j]
        if energy.bit_length() > INTEGER_CAP:
            raise ArithmeticError("verification energy exceeds the arithmetic cap")
        progress(_hex_state(binding, k + 1, flat, wu, energy))

    # All nontail rows of the preconditioned cover residual must vanish.
    # Multiplication by the finite widest-box operator then gives the J
    # actual original cover equalities; q=J sees the exact unit tail.
    for j in range(size):
        if wu[j] - d * u[j] + full[j] - flat[j] * scale:
            raise ValueError(f"original finite cover residual is nonzero at row {j}")
    guard()
    weighted_numerator = d * energy + sum(value * value for value in full)
    if weighted_numerator.bit_length() > INTEGER_CAP:
        raise ArithmeticError("verification product exceeds the arithmetic cap")
    value = Fraction(weighted_numerator, n**4 * d * scale * scale)
    a = Fraction(4, 3) - Fraction(1, 3 * n * n)
    b = 1 + value / n - 2 * depth
    ab = a * b
    for key, calculated in (("V", value), ("a", a), ("b", b), ("ab", ab)):
        if _rational(data[key]) != calculated:
            raise ValueError(f"independent exact {key} disagrees with compact witness")
    positive_b, strict_bound = b > 0, ab < target * target
    return {
        "accepted": positive_b and strict_bound,
        "a": str(a),
        "b": str(b),
        "ab": str(ab),
        "V": str(value),
        "energy": str(value),
        "cover_count": size + 1,
        "all_covers_exactly_one": True,
        "normalization": True,
        "reflection": True,
        "positive_b": positive_b,
        "exact_unit_tail": True,
        "unused_prefixes_zero": True,
        "strict_bound": strict_bound,
        "target": str(target),
        "witness_sha256": binding,
        "recurrence_recomputed": True,
        "lower_sha256": lower_digest,
        "upper_sha256": upper_digest,
        "preconditioned_cover_residual_zero": True,
        "source_bindings_are_provenance_only": True,
    }
