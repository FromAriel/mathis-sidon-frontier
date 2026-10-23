"""Finite dyadic multiplier reconstruction, without a solver or source core.

F is the nilpotent future shift on J=2*n*L coordinates. A_k=(k/n)C_k.
This module constructs explicit arrays; independent.py checks the actual
arrays by ordinary centered-box windows, without these C operators.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction

FORMAT = "mathis.sidon.symmetric_compact_witness.v1"
BOUND = Fraction(471404576987, 500000000000)
HEX = re.compile(r"-?[0-9a-f]+\Z")
INTEGER_BITS = 131072


def integer(value):
    if not isinstance(value, str) or HEX.fullmatch(value) is None:
        raise ValueError("expected a signed hexadecimal integer")
    result = int(value, 16)
    if result.bit_length() > INTEGER_BITS:
        raise ValueError("integer exceeds the replay arithmetic cap")
    return result


def parse(data):
    if not isinstance(data, dict) or set(data) != {
        "format_version",
        "n",
        "L",
        "u_bits",
        "declared_bound",
        "u0_hex",
        "provenance",
    }:
        raise ValueError("unexpected compact-witness fields")
    if data["format_version"] != FORMAT or data["declared_bound"] != str(BOUND):
        raise ValueError("unexpected compact format or stronger declaration")
    n, length, bits = data["n"], data["L"], data["u_bits"]
    if any(type(x) is not int or x < 1 for x in (n, length, bits)) or bits > 128:
        raise ValueError("invalid compact-witness dimensions or precision")
    if n > 1024 or length > 8:
        raise ValueError("dimensions exceed the fixed public replay envelope")
    raw = data["u0_hex"]
    if not isinstance(raw, list) or len(raw) != 2 * n * length:
        raise ValueError("invalid dyadic multiplier shape")
    provenance = data["provenance"]
    if not isinstance(provenance, dict) or set(provenance) != {
        "source_receipt_sha256",
        "original_dense_sha256",
        "declared_dense_sha256",
    }:
        raise ValueError("invalid compact provenance")
    if any(
        not isinstance(v, str) or re.fullmatch("[0-9a-f]{64}", v) is None
        for v in provenance.values()
    ):
        raise ValueError("invalid provenance hash")
    return n, length, bits, [integer(value) for value in raw]


def apply_a(values, n, k, transpose=False):
    size, period = len(values), 2 * n
    if k == n:
        return list(values)
    sums = [0] * size
    if transpose:
        for j in range(size):
            sums[j] = values[j] + (sums[j - period] if j >= period else 0)
        return [
            (sums[j - n + k] if j >= n - k else 0)
            - (sums[j - n - k] if j >= n + k else 0)
            for j in range(size)
        ]
    for j in range(size - 1, -1, -1):
        sums[j] = values[j] + (sums[j + period] if j + period < size else 0)
    return [
        (sums[j + n - k] if j + n - k < size else 0)
        - (sums[j + n + k] if j + n + k < size else 0)
        for j in range(size)
    ]


def repair(data, replay):
    """Build dflat and Wu from finite integer operators and repair component n."""
    n, length, bits, u = parse(data)
    size, scale = 2 * n * length, 1 << bits
    saved = replay.stage("repair")
    if saved is None:
        flat, wu, cursor = [0] * size, [0] * size, 1
    else:
        cursor = saved.get("next_k")
        if type(cursor) is not int or not 1 <= cursor <= n + 1:
            raise ValueError("invalid repair cursor")
        flat = [integer(x) for x in saved["flat_hex"]]
        wu = [integer(x) for x in saved["wu_hex"]]
        if len(flat) != size or len(wu) != size:
            raise ValueError("invalid repair checkpoint shape")
    ones = [1] * size
    for k in range(cursor, n + 1):
        forward = apply_a(ones, n, k)
        product = apply_a(apply_a(u, n, k, True), n, k)
        cflat, cw = (4 * k * k, 4 * k) if k < n else ((2 * n - 1) * n, 2 * n - 1)
        for j in range(size):
            flat[j] += cflat * forward[j]
            wu[j] += cw * product[j]
        if (
            max(max(map(int.bit_length, flat)), max(map(int.bit_length, wu)))
            > INTEGER_BITS
        ):
            raise ValueError("repair arithmetic exceeds its bit envelope")
        replay.save(
            "repair",
            {
                "next_k": k + 1,
                "flat_hex": [format(v, "x") for v in flat],
                "wu_hex": [format(v, "x") for v in wu],
            },
        )
    flat_den, wu_den = n**3, n * n * scale
    common = math.lcm(flat_den, wu_den)
    residual = [
        x * (common // flat_den) - y * (common // wu_den) for x, y in zip(flat, wu)
    ]
    correction_den = common * (2 * n - 1)
    denominator = math.lcm(scale, correction_den // math.gcd(correction_den, n * n))
    full = [
        x * (denominator // scale) + e * (n * n * denominator // correction_den)
        for x, e in zip(u, residual)
    ]
    return n, length, bits, u, full, denominator


def rows(n, length, bits, u, full, full_den, start=1):
    """Yield actual integer boundary numerators and one denominator per row."""
    scale = 1 << bits
    for k in range(start, n + 1):
        if k == n:
            yield k, list(full), full_den
        else:
            yield k, [n * value for value in apply_a(u, n, k, True)], k * scale
