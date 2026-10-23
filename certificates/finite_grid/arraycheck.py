"""Independent original-array gzip checker; Python 3.10+ standard library.

Only supplied kernel and boundary arrays determine acceptance. No construction,
compact-witness, or other verification module is imported. Two streaming passes
support arbitrary root-field order without retaining the kernel matrix. Resume
accumulators are an owner-controlled private cache: the caller must checksum
and bind checkpoints to this code. Unkeyed checksums detect accidental damage,
not adversarial replacement. Fresh/untrusted runs must supply state=None.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import math
import re
from contextlib import ExitStack
from fractions import Fraction as Q
from pathlib import Path

SCHEMA = "mathis.research.sidon.smoothing_certificate.v1"
BOUND = Q(11785113371, 12500000000)
FIELDS = {
    "format_version",
    "block_size",
    "window_length",
    "declared_bound",
    "mixing",
    "kernels",
    "boundary",
}
MAX_N, MAX_L = 2048, 32
ENTRY_BITS, ARITHMETIC_BITS = 4096, 131072
COMPRESSED_CAP, RAW_CAP = 2 * 1024**3, 32 * 1024**3
ROW_CAP = 384 * 1024**2  # Bounded value memory, including unreduced rational spellings.
RATIONAL_CHAR_CAP = 80000  # Two 131072-bit decimal integers plus sign and slash.
RATIONAL = re.compile(r"-?[0-9]+(?:/[0-9]+)?\Z")
HEX = re.compile(r"-?[0-9a-f]+\Z")


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def forbidden(value):
    raise ValueError("inexact JSON number: " + value)


def decimal(raw):
    # Avoid changing Python's process-global decimal conversion limit. Normal
    # certificate entries take the fast int path; only huge raw spellings need
    # bounded nine-digit chunks.
    if len(raw) < 4000:
        return int(raw)
    negative = raw.startswith("-")
    digits = raw[1:] if negative else raw
    result = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start : start + 9]
        result = result * (10 ** len(chunk)) + int(chunk)
        if result.bit_length() > ARITHMETIC_BITS:
            raise ValueError("raw rational exceeds 131072-bit parse envelope")
    return -result if negative else result


def parts(raw):
    if not isinstance(raw, str) or len(raw) > RATIONAL_CHAR_CAP or not RATIONAL.fullmatch(raw):
        raise ValueError("expected bounded exact rational string")
    left, separator, right = raw.partition("/")
    numerator, denominator = decimal(left), decimal(right) if separator else 1
    bits = max(abs(numerator).bit_length(), denominator.bit_length())
    if bits > ARITHMETIC_BITS or denominator <= 0:
        raise ValueError("raw rational exceeds parse envelope or denominator is nonpositive")
    divisor = math.gcd(numerator, denominator)
    numerator, denominator = numerator // divisor, denominator // divisor
    if max(abs(numerator).bit_length(), denominator.bit_length()) > ENTRY_BITS:
        raise ValueError("rational exceeds 4096-bit envelope or denominator is nonpositive")
    return numerator, denominator


def rational(raw):
    return Q(*parts(raw))


def bounded(value):
    if isinstance(value, Q):
        size = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
    else:
        size = abs(value).bit_length()
    if size > ARITHMETIC_BITS:
        raise ValueError("intermediate exceeds 131072-bit arithmetic envelope")
    return value


def weight(n, k):
    return Q(4 * k**3, n**4) if k < n else Q(2 * n - 1, n * n)


class Hashed(io.RawIOBase):
    def __init__(self, stream, cap, guard):
        super().__init__()
        self.stream, self.cap, self.guard = stream, cap, guard
        self.digest, self.count = hashlib.sha256(), 0

    def readable(self):
        return True

    def readinto(self, target):
        self.guard()
        chunk = self.stream.read(len(target))
        self.count += len(chunk)
        if self.count > self.cap:
            raise ValueError("certificate byte cap exceeded")
        self.digest.update(chunk)
        target[: len(chunk)] = chunk
        return len(chunk)


class Stream:
    """Decode one row at a time, including the otherwise enormous kernel header."""

    def __init__(self, path, guard):
        self.stack = ExitStack()
        try:
            source = self.stack.enter_context(Path(path).open("rb"))  # noqa: SIM115 - ExitStack owns the file
            self.compressed = Hashed(source, COMPRESSED_CAP, guard)
            buffered = self.stack.enter_context(io.BufferedReader(self.compressed))
            zipped = self.stack.enter_context(gzip.GzipFile(fileobj=buffered, mode="rb"))
            self.raw = Hashed(zipped, RAW_CAP, guard)
            raw_buffer = self.stack.enter_context(io.BufferedReader(self.raw))
            self.text = self.stack.enter_context(io.TextIOWrapper(raw_buffer, encoding="utf-8"))
        except Exception:
            self.stack.close()
            raise
        self.buffer, self.index, self.eof = "", 0, False
        self.decoder = json.JSONDecoder(
            object_pairs_hook=pairs, parse_float=forbidden, parse_constant=forbidden
        )

    def fill(self):
        if self.index:
            self.buffer = self.buffer[self.index :]
            self.index = 0
        chunk = self.text.read(1 << 20)
        self.buffer += chunk
        if not chunk:
            self.eof = True

    def peek(self):
        while True:
            while self.index < len(self.buffer) and self.buffer[self.index] in " \t\r\n":
                self.index += 1
            if self.index < len(self.buffer) or self.eof:
                return self.buffer[self.index : self.index + 1]
            self.fill()

    def token(self, wanted):
        if self.peek() != wanted:
            raise ValueError("malformed streaming JSON delimiter")
        self.index += 1

    def value(self, limit=65536):
        self.peek()
        while True:
            try:
                value, end = self.decoder.raw_decode(self.buffer, self.index)
            except json.JSONDecodeError as error:
                if self.eof or len(self.buffer) - self.index > limit:
                    raise ValueError("malformed or oversized JSON value") from error
                self.fill()
            else:
                if end - self.index > limit:
                    raise ValueError("oversized JSON value")
                if end == len(self.buffer) and not self.eof and type(value) is int:
                    self.fill()
                    continue
                self.index = end
                return value

    def entries(self):
        seen = set()
        self.token("{")
        while self.peek() != "}":
            if seen:
                self.token(",")
            key = self.value()
            if not isinstance(key, str) or key not in FIELDS or key in seen:
                raise ValueError("unknown or duplicate certificate field")
            seen.add(key)
            self.token(":")
            if key in ("kernels", "boundary"):
                self.token("[")
                count = 0
                while self.peek() != "]":
                    if count:
                        self.token(",")
                    row = self.value(ROW_CAP)
                    count += 1
                    cap = 2 * MAX_N if key == "kernels" else 2 * MAX_N * MAX_L
                    if count > MAX_N or not isinstance(row, list) or not 1 <= len(row) <= cap:
                        raise ValueError("array shape exceeds bounded replay envelope")
                    yield key + "_row", row
                self.token("]")
                yield key + "_count", count
            else:
                yield key, self.value()
        self.token("}")
        if self.peek() or seen != FIELDS:
            raise ValueError("trailing data or missing certificate field")

    def receipt(self):
        return {
            "sha256": self.compressed.digest.hexdigest(),
            "raw_sha256": self.raw.digest.hexdigest(),
            "compressed_bytes": self.compressed.count,
            "raw_bytes": self.raw.count,
        }

    def close(self):
        self.stack.close()


def metadata(source, expected_bound, guard):
    data, kernel_shapes, boundary_shapes = {}, [], []
    for key, value in source.entries():
        guard()
        if key == "kernels_row":
            k, m = len(kernel_shapes) + 1, len(value)
            if m % 2 or k > m // 2:
                raise ValueError("invalid centered kernel dimensions")
            n = m // 2
            cache = {}
            for j, raw in enumerate(value):
                if not isinstance(raw, str):
                    raise ValueError("kernel rational must be a string")
                if raw not in cache:
                    cache[raw] = rational(raw)
                wanted = Q(1, 2 * k) if n - k <= j < n + k else Q(0)
                if cache[raw] != wanted:
                    raise ValueError("kernel is not the nonnegative normalized centered box")
            kernel_shapes.append(m)
        elif key == "boundary_row":
            # Parsing/shape only here; entry GCDs and bit checks occur in arithmetic.
            boundary_shapes.append(len(value))
        else:
            data[key] = value
    m, length = data.get("block_size"), data.get("window_length")
    if type(m) is not int or m < 2 or m % 2 or m > 2 * MAX_N:
        raise ValueError("invalid block size")
    if type(length) is not int or not 1 <= length <= MAX_L:
        raise ValueError("invalid window length")
    n = m // 2
    if (
        data.get("format_version") != SCHEMA
        or rational(data.get("declared_bound")) != expected_bound
        or kernel_shapes != [m] * n
        or boundary_shapes != [m * length] * n
    ):
        raise ValueError("schema, declaration, or actual array dimensions mismatch")
    mixing = data.get("mixing")
    if not isinstance(mixing, list) or len(mixing) != n:
        raise ValueError("invalid mixing shape")
    weights = [rational(raw) for raw in mixing]
    if weights != [weight(n, k) for k in range(1, n + 1)] or sum(weights, Q(0)) != 1:
        raise ValueError("mixing is not the required positive probability vector")
    return n, length, weights


def _hex(raw):
    if not isinstance(raw, str) or len(raw) > ARITHMETIC_BITS // 4 + 2 or not HEX.fullmatch(raw):
        raise ValueError("invalid bounded checkpoint integer")
    return bounded(int(raw, 16))


def _restore(state, identity, size, n):
    if state is None:
        return 1, [0] * size, 1, Q(0)
    saved = copy.deepcopy(state)
    fields = {
        "identity",
        "next_k",
        "covers_hex",
        "cover_den_hex",
        "energy_num_hex",
        "energy_den_hex",
    }
    if not isinstance(saved, dict) or set(saved) != fields or saved["identity"] != identity:
        raise ValueError("array checkpoint input/code binding mismatch")
    cursor, raw = saved["next_k"], saved["covers_hex"]
    if (
        type(cursor) is not int
        or not 1 <= cursor <= n + 1
        or not isinstance(raw, list)
        or len(raw) != size
    ):
        raise ValueError("invalid array checkpoint cursor or shape")
    covers = [_hex(value) for value in raw]
    den = _hex(saved["cover_den_hex"])
    numerator, denominator = _hex(saved["energy_num_hex"]), _hex(saved["energy_den_hex"])
    if den <= 0 or denominator <= 0 or numerator < 0:
        raise ValueError("invalid array checkpoint denominator or energy")
    return cursor, covers, den, bounded(Q(numerator, denominator))


def verify(
    path,
    *,
    expected_bound=BOUND,
    expected_sha=None,
    expected_raw_sha=None,
    state=None,
    progress=lambda _: None,
    guard=lambda: None,
):
    """Recompute exact finite covers/energy from a gzip original-schema document.

    Every invocation rechecks actual input bytes and metadata. Completed arithmetic
    rows may be skipped only from the caller's trusted private checkpoint. No hash
    state or certificate-provided success value is restored. Callback arguments and
    restored mutable arrays are private copies. The external runtime binds code;
    this module also binds its own file digest in its arithmetic checkpoint.
    """
    path = Path(path).resolve(strict=True)
    if not isinstance(expected_bound, Q) or expected_bound <= 0:
        raise ValueError("expected bound must be a positive exact Fraction")
    initial_stat = path.stat()
    if initial_stat.st_size >= COMPRESSED_CAP:
        raise ValueError("compressed certificate must be smaller than 2 GiB")
    source = Stream(path, guard)
    try:
        n, length, weights = metadata(source, expected_bound, guard)
        receipt = source.receipt()
    finally:
        source.close()
    if expected_sha is not None and receipt["sha256"] != expected_sha:
        raise ValueError("compressed SHA256 mismatch")
    if expected_raw_sha is not None and receipt["raw_sha256"] != expected_raw_sha:
        raise ValueError("raw SHA256 mismatch")
    size, m = 2 * n * length, 2 * n
    identity = {
        "path": str(path),
        "sha256": receipt["sha256"],
        "raw_sha256": receipt["raw_sha256"],
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "n": n,
        "L": length,
        "bound": str(expected_bound),
    }
    cursor, covers, cover_den, energy = _restore(state, identity, size, n)

    def checkpoint(next_k):
        progress(
            {
                "identity": copy.deepcopy(identity),
                "next_k": next_k,
                "covers_hex": [format(value, "x") for value in covers],
                "cover_den_hex": format(cover_den, "x"),
                "energy_num_hex": format(energy.numerator, "x"),
                "energy_den_hex": format(energy.denominator, "x"),
            }
        )

    checkpoint(cursor)
    source = Stream(path, guard)
    count = 0
    try:
        for key, row in source.entries():
            guard()
            if key != "boundary_row":
                continue
            count += 1
            if len(row) != size or count > n:
                raise ValueError("boundary row shape changed")
            if count < cursor:
                continue
            pair_values, denominator = [], 1
            for raw in row:
                num, den = parts(raw)
                pair_values.append((num, den))
                denominator = bounded(math.lcm(denominator, den))
            values = [bounded(num * (denominator // den)) for num, den in pair_values]
            del pair_values, row
            k = count
            if any(values[: n - k]):
                raise ValueError("unused boundary prefix must be exactly zero")
            factor = bounded(weights[k - 1] / (2 * k * denominator))
            common = bounded(math.lcm(cover_den, factor.denominator))
            if common != cover_den:
                scale = common // cover_den
                covers = [bounded(value * scale) for value in covers]
            cover_den = common
            multiplier = bounded(factor.numerator * (common // factor.denominator))
            # Direct forward windows. Entries beyond the finite array are exactly
            # the prescribed unit tail; no compact operator identity is used.
            left, right = n - k, n + k
            total = bounded(sum(values[left:right]))
            for j in range(size):
                if j % 2048 == 0:
                    guard()
                covers[j] = bounded(covers[j] + bounded(multiplier * total))
                leaving = values[j + left] if j + left < size else denominator
                entering = values[j + right] if j + right < size else denominator
                total = bounded(total + entering - leaving)
            square_sum = 0
            for j, value in enumerate(values):
                if j % 2048 == 0:
                    guard()
                square_sum = bounded(square_sum + bounded(value * value))
            energy = bounded(
                energy + bounded(weights[k - 1] * Q(square_sum, bounded(denominator * denominator)))
            )
            checkpoint(k + 1)
        second_receipt = source.receipt()
    finally:
        source.close()
    final_stat = path.stat()
    if (
        count != n
        or receipt != second_receipt
        or (initial_stat.st_size, initial_stat.st_mtime_ns, initial_stat.st_ino)
        != (final_stat.st_size, final_stat.st_mtime_ns, final_stat.st_ino)
    ):
        raise ValueError("input changed during verification")
    minimum = min(min(covers), cover_den)
    a = bounded(sum((m * value / (2 * k) for k, value in enumerate(weights, 1)), Q(0)))
    b = bounded(1 + 2 * (energy / m - length))
    product = bounded(a * b)
    strict = a > 0 and b > 0 and product < expected_bound * expected_bound
    return {
        "accepted": minimum >= cover_den and strict,
        "V": str(energy),
        "energy": str(energy),
        "a": str(a),
        "b": str(b),
        "ab": str(product),
        "declared_bound": str(expected_bound),
        "block_size": m,
        "window_length": length,
        "component_count": n,
        "boundary_entries": n * size,
        "cover_count": size + 1,
        "all_covers_exactly_one": all(value == cover_den for value in covers),
        "minimum_cover_slack": str(Q(minimum - cover_den, cover_den)),
        "positive_b": b > 0,
        "strict_bound_holds": strict,
        "normalization": True,
        "reflection": True,
        "unused_prefixes_zero": True,
        "exact_unit_tail": True,
        **receipt,
    }
