"""Independent streaming array controls; run with python -I -S -m unittest."""

from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from fractions import Fraction as Q
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


array = load("finite_grid_array_controls", ROOT / "certificates/finite_grid/arraycheck.py")
generic = [
    load("finite_grid_generic_" + str(j), ROOT / "certificates" / folder / "smoothing_verify.py")
    for j, folder in enumerate(("two_sided", "two_sided_recovery"))
]


def document(n=3, length=2, varied=False):
    size, width = 2 * n * length, 2 * n
    weights = [Q(4 * k**3, n**4) if k < n else Q(2 * n - 1, n * n) for k in range(1, n + 1)]
    rows = [
        [
            Q(0) if j < n - k else Q(1) + (Q((j % 3) - 1, k + 31) if varied else 0)
            for j in range(size)
        ]
        for k in range(1, n)
    ]
    full = [Q(0)] * size
    for j in range(size - 1, -1, -1):
        other = sum(
            (
                weights[k - 1]
                * sum((row[j + i] if j + i < size else Q(1)) for i in range(n - k, n + k))
                / (2 * k)
                for k, row in enumerate(rows, 1)
            ),
            Q(0),
        )
        full[j] = width * (1 - other) / weights[-1] - sum(
            full[j + i] if j + i < size else Q(1) for i in range(1, width)
        )
    rows.append(full)
    return {
        "format_version": array.SCHEMA,
        "block_size": width,
        "window_length": length,
        "declared_bound": "10",
        "mixing": list(map(str, weights)),
        "kernels": [
            [str(Q(1, 2 * k)) if n - k <= j < n + k else "0" for j in range(width)]
            for k in range(1, n + 1)
        ],
        "boundary": [list(map(str, row)) for row in rows],
    }


class ArrayTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "tmp" / "finite_grid_array_tests"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)

    def write(self, obj=None, raw=None, name="array.json.gz", split=False):
        if raw is None:
            raw = json.dumps(obj or document(), separators=(",", ":")).encode()
        path = self.folder / name
        if split:
            mid = len(raw) // 2
            payload = gzip.compress(raw[:mid], mtime=0) + gzip.compress(raw[mid:], mtime=0)
        else:
            payload = gzip.compress(raw, mtime=0)
        path.write_bytes(payload)
        return path

    def check(self, obj=None, **kwargs):
        return array.verify(self.write(obj), expected_bound=Q(10), **kwargs)

    def test_exact_controls_against_both_unchanged_generic_checkers(self):
        for n in (1, 2, 3, 8, 16):
            for varied in (False, True):
                with self.subTest(n=n, varied=varied):
                    obj = document(n, varied=varied)
                    result = self.check(obj)
                    self.assertTrue(result["accepted"])
                    self.assertTrue(result["all_covers_exactly_one"])
                    self.assertEqual(result["cover_count"], 4 * n + 1)
                    for checker in generic:
                        cert = checker.SmoothingCertificate(
                            tuple(map(Q, obj["mixing"])),
                            tuple(tuple(map(Q, row)) for row in obj["kernels"]),
                            tuple(tuple(map(Q, row)) for row in obj["boundary"]),
                            2,
                            2 * n,
                            Q(10),
                        )
                        old = checker.verify_certificate(cert).to_dict()
                        self.assertTrue(old["checks_passed"])
                        self.assertEqual(result["a"], old["energy_constant_a"])
                        self.assertEqual(result["b"], old["boundary_constant_b"])
                        self.assertEqual(result["ab"], old["gamma_squared_ab"])

    def test_arbitrary_root_order_and_concatenated_gzip(self):
        obj = document()
        result = array.verify(
            self.write(dict(reversed(list(obj.items()))), split=True), expected_bound=Q(10)
        )
        self.assertTrue(result["accepted"])

    def test_actual_byte_hashes(self):
        path = self.write()
        payload = path.read_bytes()
        sha, raw_sha = (
            hashlib.sha256(payload).hexdigest(),
            hashlib.sha256(gzip.decompress(payload)).hexdigest(),
        )
        result = array.verify(
            path, expected_bound=Q(10), expected_sha=sha, expected_raw_sha=raw_sha
        )
        self.assertEqual(result["sha256"], sha)
        self.assertEqual(result["raw_sha256"], raw_sha)
        self.assertEqual(result["compressed_bytes"], len(payload))
        self.assertEqual(result["raw_bytes"], len(gzip.decompress(payload)))
        for keyword in ("expected_sha", "expected_raw_sha"):
            with self.subTest(keyword=keyword), self.assertRaises(ValueError):
                array.verify(path, expected_bound=Q(10), **{keyword: "0" * 64})

    def test_large_unreduced_rationals_keep_reduced_entry_cap(self):
        # 18001 decimal digits exceeds Python's default int conversion limit.
        huge = "1" + "0" * 18000
        self.assertEqual(array.parts(huge + "/" + huge), (1, 1))
        obj = document()
        obj["boundary"][-1][0] = huge + "/" + huge
        self.assertTrue(self.check(obj)["accepted"])
        self.assertEqual(array.parts("6/6"), (1, 1))
        # Distinct prime exponents give pairwise coprime Mersenne denominators.
        # Their unreduced LCM exceeds the intermediate cap although each value
        # equals one and each raw input lies inside the ordinary entry cap.
        exponents = [p for p in range(3500, 4096) if all(p % d for d in range(2, int(p**0.5) + 1))][
            :64
        ]
        self.assertEqual(len(exponents), 64)
        obj = document(16)
        obj["boundary"][-1] = [(str((1 << p) - 1) + "/" + str((1 << p) - 1)) for p in exponents]
        self.assertTrue(self.check(obj)["accepted"])
        for raw in (huge + "/3", "1" + "0" * 40000, "1/" + "1" + "0" * 40000):
            with self.subTest(prefix=raw[:8]), self.assertRaises(ValueError):
                array.parts(raw)

    def test_resume_and_completed_math_skip(self):
        path, saved = self.write(document(8, varied=True)), []

        def interrupt(state):
            saved.append(copy.deepcopy(state))
            if state["next_k"] == 4:
                raise InterruptedError("control")

        with self.assertRaises(InterruptedError):
            array.verify(path, expected_bound=Q(10), progress=interrupt)
        before = copy.deepcopy(saved[-1])
        resumed = array.verify(path, expected_bound=Q(10), state=before, progress=saved.append)
        self.assertEqual(before, saved[3])
        with patch.object(array, "parts", wraps=array.parts) as parsed:
            completed = array.verify(path, expected_bound=Q(10), state=saved[-1])
            resumed_calls = parsed.call_count
        with patch.object(array, "parts", wraps=array.parts) as parsed:
            fresh = array.verify(path, expected_bound=Q(10))
            self.assertEqual(parsed.call_count - resumed_calls, 8 * 32)
        self.assertEqual(resumed, fresh)
        self.assertEqual(completed, fresh)

    def test_callback_values_do_not_alias_accumulators(self):
        path = self.write()

        def mutate(state):
            state["covers_hex"][0] = "dead"
            state["identity"]["n"] = 0

        self.assertEqual(
            array.verify(path, expected_bound=Q(10), progress=mutate),
            array.verify(path, expected_bound=Q(10)),
        )

    def test_checkpoint_binding_shape_and_integer_caps(self):
        path, saved = self.write(), []
        array.verify(path, expected_bound=Q(10), progress=saved.append)
        for field, value in (
            ("next_k", True),
            ("covers_hex", []),
            ("cover_den_hex", "0"),
            ("energy_den_hex", "-1"),
            ("energy_num_hex", "-1"),
        ):
            state = copy.deepcopy(saved[-1])
            state[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                array.verify(path, expected_bound=Q(10), state=state)
        for field in ("sha256", "raw_sha256", "code_sha256", "path", "bound", "n", "L"):
            state = copy.deepcopy(saved[-1])
            state["identity"][field] = "wrong"
            with self.subTest(field=field), self.assertRaises(ValueError):
                array.verify(path, expected_bound=Q(10), state=state)
        state = copy.deepcopy(saved[-1])
        state["covers_hex"][0] = "f" * 32769
        with self.assertRaises(ValueError):
            array.verify(path, expected_bound=Q(10), state=state)

    def test_guard_interrupts(self):
        def guard():
            raise InterruptedError("guard")

        with self.assertRaises(InterruptedError):
            self.check(guard=guard)

    def test_cover_and_strict_bound_failures(self):
        obj = document()
        obj["boundary"][-1][0] = "-100"
        result = self.check(obj)
        self.assertFalse(result["accepted"])
        self.assertFalse(result["all_covers_exactly_one"])
        obj = document(1)
        obj["declared_bound"] = "1"
        self.assertFalse(array.verify(self.write(obj), expected_bound=Q(1))["accepted"])

    def test_metadata_mutations(self):
        cases = [
            ("block_size", True),
            ("block_size", 3),
            ("block_size", 4098),
            ("window_length", 0),
            ("window_length", 33),
            ("format_version", "wrong"),
            ("declared_bound", "9"),
            ("mixing", ["1"]),
            ("boundary", []),
            ("kernels", []),
        ]
        for key, value in cases:
            obj = document()
            obj[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.check(obj)

    def test_actual_row_mutations(self):
        for which, raw in (
            ("kernels", "-1"),
            ("kernels", "0.5"),
            ("boundary", "1/0"),
            ("boundary", 1),
            ("boundary", "1.0"),
            ("boundary", "1/" + str(1 << 4096)),
        ):
            obj = document()
            obj[which][0][-1] = raw
            with self.subTest(which=which, raw=str(raw)[:20]), self.assertRaises(ValueError):
                self.check(obj)
        obj = document()
        obj["boundary"][0][0] = "1"
        with self.assertRaises(ValueError):
            self.check(obj)
        obj = document()
        obj["boundary"][0].pop()
        with self.assertRaises(ValueError):
            self.check(obj)

    def test_duplicate_unknown_missing_and_inexact_json(self):
        raw = json.dumps(document()).encode()
        for bad in (
            b'{"block_size":6,' + raw[1:],
            raw[:-1] + b',"unknown":0}',
            raw.replace(b'"window_length": 2,', b""),
            raw + b"{}",
            raw.replace(b'"window_length": 2', b'"window_length": 2.0'),
            raw.replace(b'"window_length": 2', b'"window_length": NaN'),
        ):
            with self.subTest(prefix=bad[:40]), self.assertRaises(ValueError):
                array.verify(self.write(raw=bad), expected_bound=Q(10))

    def test_truncated_corrupt_and_non_gzip(self):
        for payload in (self.write().read_bytes()[:-8], b"not gzip", b"\x1f\x8b"):
            path = self.folder / "broken.gz"
            path.write_bytes(payload)
            with (
                self.subTest(payload=payload[:8]),
                self.assertRaises((ValueError, OSError, EOFError)),
            ):
                array.verify(path, expected_bound=Q(10))
        path = self.write()
        raw = bytearray(path.read_bytes())
        raw[-8] ^= 1
        path.write_bytes(raw)
        with self.assertRaises((ValueError, OSError, EOFError)):
            array.verify(path, expected_bound=Q(10))

    def test_byte_value_and_arithmetic_caps(self):
        path = self.write()
        for cap in ("COMPRESSED_CAP", "RAW_CAP", "ROW_CAP"):
            with self.subTest(cap=cap), patch.object(array, cap, 32), self.assertRaises(ValueError):
                array.verify(path, expected_bound=Q(10))
        with patch.object(array, "ARITHMETIC_BITS", 4), self.assertRaises(ValueError):
            array.verify(path, expected_bound=Q(10))
        with self.assertRaises(ValueError):
            array.parts(str(1 << 4096))

    def test_dimensions_after_oversized_rows(self):
        obj = document()
        obj["boundary"][0] = ["0"] * (2 * array.MAX_N * array.MAX_L + 1)
        obj = {"boundary": obj.pop("boundary"), **obj}
        with self.assertRaises(ValueError):
            self.check(obj)

    def test_file_changes_during_math_are_detected(self):
        path = self.write()

        def change(state):
            if state["next_k"] == 1:
                path.write_bytes(path.read_bytes() + b"junk")

        with self.assertRaises((ValueError, OSError, EOFError)):
            array.verify(path, expected_bound=Q(10), progress=change)


if __name__ == "__main__":
    unittest.main()
