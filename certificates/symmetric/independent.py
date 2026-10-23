"""Actual-array centered-box verification; Python 3.10+ standard library only.

This module imports no multiplier construction or sparse C-operator helper.
It sums ordinary forward box windows of the supplied boundary entries and
recomputes weighted energy. Free boundary entries may have either sign.
"""

from __future__ import annotations

import json
import math
import re
from fractions import Fraction
from pathlib import Path

SCHEMA = "mathis.research.sidon.smoothing_certificate.v1"
FIELDS = {
    "format_version",
    "block_size",
    "window_length",
    "declared_bound",
    "mixing",
    "kernels",
    "boundary",
}
RATIONAL = re.compile(r"-?[0-9]+(?:/[0-9]+)?\Z")
RATIONAL_BITS = 4096
ARITHMETIC_BITS = 131072


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def forbidden(value):
    raise ValueError("inexact JSON number: " + value)


def fraction_parts(raw):
    if not isinstance(raw, str) or len(raw) > 2500 or RATIONAL.fullmatch(raw) is None:
        raise ValueError("expected a bounded exact rational string")
    if "/" in raw:
        left, right = raw.split("/")
        numerator, denominator = int(left), int(right)
    else:
        numerator, denominator = int(raw), 1
    if denominator <= 0:
        raise ValueError("rational denominator must be positive")
    if max(numerator.bit_length(), denominator.bit_length()) > RATIONAL_BITS:
        raise ValueError("rational exceeds the unchanged 4096-bit acceptance cap")
    return numerator, denominator


def rational(raw):
    return Fraction(*fraction_parts(raw))


def weight(n, k):
    return Fraction(4 * k**3, n**4) if k < n else Fraction(2 * n - 1, n * n)


def check_rows(n, length, bound, rows, replay, on_row=None):
    """Check supplied actual rows, with exact direct prefixes and square sums."""
    if any(type(x) is not int or x < 1 for x in (n, length)) or n > 1024 or length > 8:
        raise ValueError("invalid centered-box replay dimensions")
    if not isinstance(bound, Fraction) or bound <= 0:
        raise ValueError("declared bound must be a positive exact rational")
    size, m = 2 * n * length, 2 * n
    mixing = [weight(n, k) for k in range(1, n + 1)]
    if any(x <= 0 for x in mixing) or sum(mixing, Fraction(0)) != 1:
        raise ValueError("mixing is not a positive probability vector")
    # Each actual implicit kernel has 2k nonnegative entries 1/(2k), at the
    # centered support n-k,...,n+k-1. Its reflection and normalization are exact.
    a = sum((m * value / (2 * k) for k, value in enumerate(mixing, 1)), Fraction(0))
    saved = replay.stage("verification")
    if saved is None:
        cursor, covers, cover_den, energy, max_bits = 1, [0] * size, 1, Fraction(0), 0
    else:
        cursor = saved.get("next_k")
        if type(cursor) is not int or not 1 <= cursor <= n + 1:
            raise ValueError("invalid actual-array verification cursor")
        covers = [int(x, 16) for x in saved["covers_hex"]]
        cover_den = int(saved["cover_den_hex"], 16)
        energy = rational(saved["energy"])
        max_bits = saved["max_raw_rational_bits"]
        if len(covers) != size or cover_den <= 0:
            raise ValueError("invalid actual-array checkpoint shape")
    count = cursor - 1
    for k, values, denominator in rows:
        if (
            k != count + 1
            or k > n
            or len(values) != size
            or type(denominator) is not int
            or denominator <= 0
        ):
            raise ValueError("actual boundary row shape/order mismatch")
        if any(type(value) is not int for value in values):
            raise ValueError("actual boundary numerator is not an integer")
        raw_bits = max(
            denominator.bit_length(), max(map(int.bit_length, values), default=0)
        )
        if raw_bits > RATIONAL_BITS:
            # Public row common denominators can be larger than individual
            # reduced fractions. Check those values before rejecting them.
            for value in values:
                reduced = Fraction(value, denominator)
                if (
                    max(
                        reduced.numerator.bit_length(), reduced.denominator.bit_length()
                    )
                    > RATIONAL_BITS
                ):
                    raise ValueError(
                        "actual boundary exceeds the unchanged rational cap"
                    )
        max_bits = max(max_bits, raw_bits)
        if any(value != 0 for value in values[: n - k]):
            raise ValueError("unused boundary prefix must be exactly zero")
        factor = mixing[k - 1] / (2 * k * denominator)
        common = math.lcm(cover_den, factor.denominator)
        if common.bit_length() > ARITHMETIC_BITS:
            raise ValueError("cover arithmetic exceeds replay resource envelope")
        if common != cover_den:
            multiplier = common // cover_den
            covers = [value * multiplier for value in covers]
        cover_den = common
        multiplier = factor.numerator * (cover_den // factor.denominator)
        prefix = [0]
        for value in values + [denominator] * m:
            prefix.append(prefix[-1] + value)
        for j in range(size):
            covers[j] += multiplier * (prefix[j + n + k] - prefix[j + n - k])
        square_sum = sum(value * value for value in values)
        energy += mixing[k - 1] * Fraction(square_sum, denominator * denominator)
        if on_row is not None:
            on_row(k, values, denominator)
        count += 1
        replay.save(
            "verification",
            {
                "next_k": k + 1,
                "covers_hex": [format(value, "x") for value in covers],
                "cover_den_hex": format(cover_den, "x"),
                "energy": str(energy),
                "max_raw_rational_bits": max_bits,
            },
        )
    if count != n:
        raise ValueError("missing actual boundary component")
    # At q=J all accesses are unit tails: the final cover is sum lambda=1.
    minimum = min(min(covers), cover_den)
    b = 1 + 2 * (energy / m - length)
    product = a * b
    covered = minimum >= cover_den
    strict = b > 0 and a > 0 and product < bound * bound
    return {
        "accepted": covered and strict,
        "a": str(a),
        "b": str(b),
        "ab": str(product),
        "energy": str(energy),
        "declared_bound": str(bound),
        "block_size": m,
        "window_length": length,
        "component_count": n,
        "boundary_entries": n * size,
        "cover_count": size + 1,
        "all_covers_exactly_one": all(value == cover_den for value in covers),
        "minimum_cover_slack": str(Fraction(minimum - cover_den, cover_den)),
        "positive_b": b > 0,
        "strict_bound_holds": strict,
        "normalization": True,
        "reflection": True,
        "unused_prefixes_zero": True,
        "exact_unit_tail": True,
    }


class Stream:
    """Incremental standard-library JSON reader, never loading the boundary map."""

    def __init__(self, path):
        self.stream = Path(path).open("r", encoding="utf-8")  # noqa: SIM115 - closed by entries() finally
        self.buffer, self.index, self.eof = "", 0, False
        self.decoder = json.JSONDecoder(
            object_pairs_hook=object_pairs,
            parse_float=forbidden,
            parse_constant=forbidden,
        )

    def fill(self):
        if self.index:
            self.buffer = self.buffer[self.index :]
            self.index = 0
        chunk = self.stream.read(1 << 20)
        self.buffer += chunk
        if not chunk:
            self.eof = True

    def whitespace(self):
        while True:
            while self.index < len(self.buffer) and self.buffer[self.index].isspace():
                self.index += 1
            if self.index < len(self.buffer) or self.eof:
                return
            self.fill()

    def token(self, expected):
        self.whitespace()
        if self.buffer[self.index : self.index + 1] != expected:
            raise ValueError("malformed streaming JSON delimiter")
        self.index += 1

    def peek(self):
        self.whitespace()
        return self.buffer[self.index : self.index + 1]

    def value(self):
        self.whitespace()
        while True:
            try:
                value, end = self.decoder.raw_decode(self.buffer, self.index)
            except json.JSONDecodeError as error:
                if self.eof or len(self.buffer) - self.index > 32 * (1 << 20):
                    raise ValueError(
                        "malformed or oversized streaming JSON value"
                    ) from error
                self.fill()
            else:
                # A number at the buffer edge could be only its first digits.
                if (
                    end == len(self.buffer)
                    and not self.eof
                    and type(value) in (int, float)
                ):
                    self.fill()
                    continue
                self.index = end
                return value

    def finish(self):
        self.whitespace()
        if self.peek():
            raise ValueError("trailing data after certificate JSON")

    def close(self):
        self.stream.close()


def entries(path):
    """Yield top-level fields; boundary rows are individual streaming events."""
    source, seen = Stream(path), set()
    try:
        source.token("{")
        while source.peek() != "}":
            if seen:
                source.token(",")
            key = source.value()
            if not isinstance(key, str) or key in seen or key not in FIELDS:
                raise ValueError("unknown or duplicate actual certificate field")
            seen.add(key)
            source.token(":")
            if key == "boundary":
                source.token("[")
                count = 0
                while source.peek() != "]":
                    if count:
                        source.token(",")
                    row = source.value()
                    if not isinstance(row, list):
                        raise ValueError("actual boundary component is not an array")
                    count += 1
                    yield "boundary_row", row
                source.token("]")
                yield "boundary_count", count
            else:
                yield key, source.value()
        source.token("}")
        source.finish()
        if seen != FIELDS:
            raise ValueError("missing actual certificate field")
    finally:
        source.close()


def metadata(path, expected_bound, heartbeat=lambda: None):
    """Separate streaming pass supports every ordering of original root fields."""
    data = {}
    for key, value in entries(path):
        heartbeat()
        if key != "boundary_row":
            data[key] = value
    m, length = data.get("block_size"), data.get("window_length")
    if type(m) is not int or m < 2 or m % 2 or type(length) is not int or length < 1:
        raise ValueError("actual dimensions do not describe centered boxes")
    n = m // 2
    if n > 1024 or length > 8 or data.get("boundary_count") != n:
        raise ValueError("actual component count/dimensions exceed replay envelope")
    if (
        data.get("format_version") != SCHEMA
        or rational(data.get("declared_bound")) != expected_bound
    ):
        raise ValueError("actual format or required stronger declaration mismatch")
    mixing, kernels = data.get("mixing"), data.get("kernels")
    if (
        not isinstance(mixing, list)
        or not isinstance(kernels, list)
        or len(mixing) != n
        or len(kernels) != n
    ):
        raise ValueError("actual kernel/mixing shape mismatch")
    for k, (raw_weight, row) in enumerate(zip(mixing, kernels), 1):
        if (
            rational(raw_weight) != weight(n, k)
            or not isinstance(row, list)
            or len(row) != m
        ):
            raise ValueError("actual weight/kernel length mismatch")
        for j, raw in enumerate(row):
            wanted = Fraction(1, 2 * k) if n - k <= j < n + k else Fraction(0)
            if rational(raw) != wanted:
                raise ValueError("actual kernel is not the nonnegative centered box")
    return n, length


def boundary_rows(path, n, length, start=1):
    count = 0
    for key, value in entries(path):
        if key != "boundary_row":
            continue
        count += 1
        if len(value) != 2 * n * length:
            raise ValueError("actual boundary length differs from L*M")
        if count < start:
            continue
        parts = [fraction_parts(raw) for raw in value]
        denominator = 1
        for _, divisor in parts:
            denominator = math.lcm(denominator, divisor)
            if denominator.bit_length() > ARITHMETIC_BITS:
                raise ValueError(
                    "actual row common denominator exceeds replay resource envelope"
                )
        yield (
            count,
            [numerator * (denominator // divisor) for numerator, divisor in parts],
            denominator,
        )
