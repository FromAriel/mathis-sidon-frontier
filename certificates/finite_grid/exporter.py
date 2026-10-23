"""Lossless compact-to-original gzip export; Python 3.10+, stdlib only.

This serializes the given exact integers. It performs no optimization or new
renewal construction. Complete gzip members are authenticated resume units.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import io
import itertools
import json
import math
import os
from fractions import Fraction as Q
from pathlib import Path

FORMAT = "mathis.research.sidon.smoothing_certificate.v1"


def prefix(values):
    result = [0]
    for value in values:
        result.append(result[-1] + value)
    return result


def raw_row(sums, n, k):
    size, shift = 2 * (len(sums) - 1), n - k
    row = [0] * shift
    for j in range(shift, size):
        end = (j - shift) // 2 + 1
        row.append(sums[end] - sums[max(0, end - k)])
    return row


def _validate_member(payload, record, guard):
    """Authenticate raw metadata by actual bounded decompression, not hash composition."""
    digest, size = hashlib.sha256(), 0
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
            for chunk in iter(lambda: stream.read(1 << 20), b""):
                guard()
                size += len(chunk)
                if size > record["raw_size"]:
                    raise ValueError("committed gzip raw length mismatch")
                digest.update(chunk)
    except (OSError, EOFError) as error:
        raise ValueError("committed gzip member is invalid") from error
    if size != record["raw_size"] or digest.hexdigest() != record["raw_sha256"]:
        raise ValueError("committed gzip raw hash or length mismatch")


def _token(value, denominator):
    common = math.gcd(value, denominator)
    num, den = value // common, denominator // common
    if max(abs(num).bit_length(), den.bit_length()) > 4096:
        raise ArithmeticError("certificate rational exceeds 4096 bits")
    return '"' + str(num) + ("/" + str(den) if den != 1 else "") + '"'


def _row(values, denominator):
    yield b"["
    pieces, previous, last = [], None, None
    for j, value in enumerate(values):
        if value != previous or last is None:
            last, previous = _token(value, denominator), value
        pieces.append(("," if j else "") + last)
        if len(pieces) == 2048:
            yield "".join(pieces).encode("ascii")
            pieces.clear()
    if pieces:
        yield "".join(pieces).encode("ascii")
    yield b"]"


def _header(n, depth, target):
    head = {
        "format_version": FORMAT,
        "block_size": 2 * n,
        "window_length": depth,
        "declared_bound": target,
        "mixing": [
            str(Q(4 * k**3, n**4) if k < n else Q(2 * n - 1, n**2)) for k in range(1, n + 1)
        ],
    }
    yield (json.dumps(head, separators=(",", ":"))[:-1] + ',"kernels":[').encode()
    for k in range(1, n + 1):
        if k > 1:
            yield b","
        yield from _row((int(n - k <= j < n + k) for j in range(2 * n)), 2 * k)
    yield b'],"boundary":['


def export(
    derivation,
    path,
    scratch,
    *,
    state=None,
    progress=lambda _: None,
    guard=lambda: None,
    compressed_cap=2 * 1024**3,
    raw_cap=32 * 1024**3,
):
    """Only the authenticated new partial stream may be truncated on resume."""
    if any(type(cap) is not int or cap < 1 for cap in (compressed_cap, raw_cap)):
        raise ValueError("export caps must be positive integers")
    path, scratch = Path(path).resolve(), Path(scratch).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".partial")
    member = scratch / "export.member.partial.gz"
    binding = hashlib.sha256(
        json.dumps(derivation, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    identity = {
        "input": binding,
        "output": str(path),
        "compressed_cap": compressed_cap,
        "raw_cap": raw_cap,
    }
    saved = copy.deepcopy(state)
    if saved is None:
        if path.exists() or partial.exists():
            raise ValueError("export output exists without authenticated state")
        records = []
        # Persist this empty binding before any bytes: a first-member crash
        # must still have an authenticated offset zero from which to restart.
        progress({"identity": copy.deepcopy(identity), "records": [], "next_k": 0})
    else:
        if (
            not isinstance(saved, dict)
            or set(saved) != {"identity", "records", "next_k"}
            or saved["identity"] != identity
            or not isinstance(saved["records"], list)
            or type(saved["next_k"]) is not int
            or saved["next_k"] != len(saved["records"])
        ):
            raise ValueError("export checkpoint identity mismatch")
        records = saved["records"]
    if path.exists() and partial.exists():
        raise ValueError("completed output conflicts with partial stream")
    n, depth, p = derivation["n"], derivation["L"], derivation["p"]
    if len(records) > n + 2:
        raise ValueError("too many gzip member records")
    offset, raw_total = 0, 0
    existing = path if path.exists() else partial
    if records:
        with existing.open("rb") as stream:
            for index, record in enumerate(records):
                guard()
                expected_kind = (
                    "header" if index == 0 else ("footer" if index == n + 1 else "component")
                )
                fields = {"offset", "size", "sha256", "raw_size", "raw_sha256", "kind"}
                if expected_kind == "component":
                    fields.add("k")
                if not isinstance(record, dict) or set(record) != fields:
                    raise ValueError("invalid gzip member record")
                if any(type(record[key]) is not int for key in ("offset", "size", "raw_size")):
                    raise ValueError("invalid gzip member size or offset")
                if record["size"] < 1 or record["raw_size"] < 1:
                    raise ValueError("invalid gzip member length")
                if any(
                    not isinstance(record[key], str)
                    or len(record[key]) != 64
                    or any(char not in "0123456789abcdef" for char in record[key])
                    for key in ("sha256", "raw_sha256")
                ):
                    raise ValueError("invalid gzip member digest")
                if record["offset"] != offset or record["kind"] != expected_kind:
                    raise ValueError("gzip record coverage mismatch")
                if expected_kind == "component" and (
                    type(record["k"]) is not int or record["k"] != index
                ):
                    raise ValueError("gzip component cursor mismatch")
                if (
                    offset + record["size"] > compressed_cap
                    or raw_total + record["raw_size"] > raw_cap
                ):
                    raise MemoryError("committed gzip prefix exceeds configured caps")
                payload = stream.read(record["size"])
                if (
                    len(payload) != record["size"]
                    or hashlib.sha256(payload).hexdigest() != record["sha256"]
                ):
                    raise ValueError("committed gzip prefix corruption")
                _validate_member(payload, record, guard)
                offset += record["size"]
                raw_total += record["raw_size"]
        if path.exists() and (len(records) != n + 2 or path.stat().st_size != offset):
            raise ValueError("unexpected completed output")
    elif existing.exists():
        if path.exists():
            raise ValueError("unbound completed output")
    if partial.exists():
        with partial.open("r+b") as stream:
            stream.truncate(offset)
    qp = prefix([int(v, 16) for v in derivation["coarse_y_hex"]])
    for index in range(len(records), n + 2):
        guard()
        if index == 0:
            chunks, kind = _header(n, depth, derivation["target"]), "header"
        elif index == n + 1:
            chunks, kind = iter([b"]}\n"]), "footer"
        else:
            k, kind = index, "component"
            if k == n:
                values = (int(v, 16) for v in derivation["full_hex"])
                denominator = int(derivation["full_den_hex"], 16)
            else:
                values, denominator = raw_row(qp, n, k), k * (1 << p)
            row = _row(values, denominator)
            chunks = iter([b","] if index > 1 else [])
            chunks = itertools.chain(chunks, row)
        raw_hash, raw_size = hashlib.sha256(), 0
        with member.open("wb") as output:
            with gzip.GzipFile(
                filename="", mode="wb", compresslevel=9, mtime=0, fileobj=output
            ) as compressor:
                for chunk in chunks:
                    raw_size += len(chunk)
                    if raw_total + raw_size > raw_cap:
                        raise MemoryError("logical decompressed JSON exceeds cap")
                    raw_hash.update(chunk)
                    compressor.write(chunk)
                    guard()
            output.flush()
            os.fsync(output.fileno())
        payload = member.read_bytes()
        if offset + len(payload) > compressed_cap:
            raise MemoryError("compressed final artifact exceeds cap")
        with partial.open("ab") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        record = {
            "offset": offset,
            "size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "raw_size": raw_size,
            "raw_sha256": raw_hash.hexdigest(),
            "kind": kind,
        }
        if kind == "component":
            record["k"] = index
        records.append(record)
        offset += len(payload)
        raw_total += raw_size
        progress(
            {
                "identity": copy.deepcopy(identity),
                "records": copy.deepcopy(records),
                "next_k": index + 1,
            }
        )
    if partial.exists():
        os.replace(partial, path)
    raw_hash, compressed_hash, actual_raw_size = hashlib.sha256(), hashlib.sha256(), 0
    with gzip.open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            guard()
            actual_raw_size += len(chunk)
            if actual_raw_size > raw_cap:
                raise MemoryError("logical decompressed JSON exceeds cap")
            raw_hash.update(chunk)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            guard()
            compressed_hash.update(chunk)
    if actual_raw_size != raw_total:
        raise ValueError("gzip raw byte count mismatch")
    return {
        "path": str(path),
        "sha256": compressed_hash.hexdigest(),
        "raw_sha256": raw_hash.hexdigest(),
        "bytes": offset,
        "raw_bytes": raw_total,
        "members": len(records),
        "original_schema": FORMAT,
    }
