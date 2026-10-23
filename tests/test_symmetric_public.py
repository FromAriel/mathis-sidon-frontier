"""Standard-library controls/rejections for the public symmetric package."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "certificates" / "symmetric"
SPEC = importlib.util.spec_from_file_location(
    "symmetric_public_wrapper", PACKAGE / "verify.py"
)
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


def data(n=2, length=1, bits=5):
    return {
        "format_version": verify.construction.FORMAT,
        "n": n,
        "L": length,
        "u_bits": bits,
        "declared_bound": str(verify.BOUND),
        "u0_hex": [format((j % 5 - 2) * 3, "x") for j in range(2 * n * length)],
        "provenance": {
            key: "0" * 64
            for key in (
                "source_receipt_sha256",
                "original_dense_sha256",
                "declared_dense_sha256",
            )
        },
    }


def parameters(witness):
    session = verify.runtime.Replay(None, {})
    return verify.construction.repair(witness, session)


def document(witness):
    values = parameters(witness)
    n, length = values[:2]
    return {
        "format_version": verify.independent.SCHEMA,
        "block_size": 2 * n,
        "window_length": length,
        "declared_bound": "10",
        "mixing": [str(verify.independent.weight(n, k)) for k in range(1, n + 1)],
        "kernels": [
            [str(F(1, 2 * k)) if n - k <= j < n + k else "0" for j in range(2 * n)]
            for k in range(1, n + 1)
        ],
        "boundary": [
            [str(F(value, denominator)) for value in row]
            for _, row, denominator in verify.construction.rows(*values)
        ],
    }


class SymmetricPublicTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "tmp" / "symmetric_public_tests"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)

    def write(self, value, name="array.json"):
        path = self.folder / name
        path.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")
        return path

    def direct_check(self, value, bound=F(10)):
        path = self.write(value)
        n, length = verify.independent.metadata(path, bound)
        return verify.independent.check_rows(
            n,
            length,
            bound,
            verify.independent.boundary_rows(path, n, length),
            verify.runtime.Replay(None, {}),
        )

    def test_literal_dense_controls(self):
        for n, length in ((1, 1), (2, 1), (3, 1), (3, 2), (8, 1), (16, 1)):
            with self.subTest(n=n, length=length):
                witness = data(n, length)
                values = parameters(witness)
                rows = list(verify.construction.rows(*values))
                result = verify.independent.check_rows(
                    n, length, F(10), iter(rows), verify.runtime.Replay(None, {})
                )
                boundaries = [[F(value, den) for value in row] for _, row, den in rows]
                weights = [
                    F(4 * k**3, n**4) if k < n else F(2 * n - 1, n * n)
                    for k in range(1, n + 1)
                ]
                energy = sum(
                    weights[k] * sum(x * x for x in row)
                    for k, row in enumerate(boundaries)
                )
                for j in range(2 * n * length + 1):
                    cover = F(0)
                    for k, row in enumerate(boundaries, 1):
                        cover += (
                            weights[k - 1]
                            * sum(
                                (row[j + i] if j + i < len(row) else F(1))
                                for i in range(n - k, n + k)
                            )
                            / (2 * k)
                        )
                    self.assertEqual(cover, 1)
                self.assertEqual(F(result["energy"]), energy)
                self.assertTrue(result["accepted"])
                self.assertTrue(result["all_covers_exactly_one"])
                actual = self.direct_check(document(witness))
                self.assertEqual(actual, result)

    def test_sparse_adjoint_against_literal_matrix(self):
        for n in (1, 2, 3, 8):
            length, values = 2, [j - n for j in range(4 * n)]
            for k in range(1, n + 1):
                size = len(values)
                matrix = [[0] * size for _ in range(size)]
                for j in range(size):
                    for r in range(length):
                        for shift, sign in (
                            (n - k + 2 * n * r, 1),
                            (n + k + 2 * n * r, -1),
                        ):
                            if j + shift < size:
                                matrix[j][j + shift] += sign
                forward = [sum(x * y for x, y in zip(row, values)) for row in matrix]
                adjoint = [
                    sum(matrix[i][j] * values[i] for i in range(size))
                    for j in range(size)
                ]
                self.assertEqual(verify.construction.apply_a(values, n, k), forward)
                self.assertEqual(
                    verify.construction.apply_a(values, n, k, True), adjoint
                )

    def test_signed_free_boundaries_are_accepted(self):
        value = document(data(3))
        self.assertTrue(any(F(x) < 0 for row in value["boundary"] for x in row))
        self.assertTrue(self.direct_check(value)["accepted"])

    def test_original_root_key_order_is_not_required(self):
        value = document(data(2))
        reordered = {"boundary": value.pop("boundary"), **value}
        self.assertTrue(self.direct_check(reordered)["accepted"])

    def test_actual_array_rejections(self):
        original = document(data())
        for mutation in (
            "kernel",
            "mixing",
            "declaration",
            "prefix",
            "row_length",
            "component_count",
            "unknown",
            "format",
            "float",
            "rational",
            "zero_denominator",
            "bit_cap",
        ):
            with self.subTest(mutation=mutation):
                value = copy.deepcopy(original)
                if mutation == "kernel":
                    value["kernels"][0][0] = "-1"
                elif mutation == "mixing":
                    value["mixing"][0] = "-1"
                elif mutation == "declaration":
                    value["declared_bound"] = "11"
                elif mutation == "prefix":
                    value["boundary"][0][0] = "1"
                elif mutation == "row_length":
                    value["boundary"][0].append("1")
                elif mutation == "component_count":
                    value["boundary"].append(value["boundary"][0])
                elif mutation == "unknown":
                    value["saved_accepted"] = True
                elif mutation == "format":
                    value["format_version"] = "other"
                elif mutation == "float":
                    value["boundary"][0][1] = 0.5
                elif mutation == "rational":
                    value["boundary"][0][1] = "1/-2"
                elif mutation == "zero_denominator":
                    value["boundary"][0][1] = "1/0"
                else:
                    value["boundary"][0][1] = str(1 << 4096)
                with self.assertRaises((ValueError, TypeError)):
                    self.direct_check(value)

    def test_duplicate_and_trailing_json_rejections(self):
        value = document(data())
        raw = json.dumps(value)
        for text in (
            raw[:-1] + ',"block_size":4}',
            raw + " {}",
            raw.replace('"boundary": [', '"boundary": [,'),
        ):
            with self.subTest(text=text[:40]):
                path = self.folder / "bad.json"
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    verify.independent.metadata(path, F(10))

    def test_bad_coverage_and_insufficient_declaration_fail_mathematically(self):
        value = document(data())
        value["boundary"][-1][-1] = "-100"
        self.assertFalse(self.direct_check(value)["accepted"])
        value = document(data())
        value["declared_bound"] = "1/2"
        self.assertFalse(self.direct_check(value, F(1, 2))["accepted"])

    def test_compact_input_rejections(self):
        for mutation in (
            "float",
            "unknown",
            "bound",
            "hex",
            "shape",
            "dimension",
            "provenance",
        ):
            with self.subTest(mutation=mutation):
                value = data()
                if mutation == "float":
                    value["u_bits"] = 5.0
                elif mutation == "unknown":
                    value["accepted"] = True
                elif mutation == "bound":
                    value["declared_bound"] = "1"
                elif mutation == "hex":
                    value["u0_hex"][0] = "0x10"
                elif mutation == "shape":
                    value["u0_hex"].pop()
                elif mutation == "dimension":
                    value["n"] = True
                else:
                    value["provenance"]["declared_dense_sha256"] = "bad"
                with self.assertRaises(ValueError):
                    verify.construction.parse(value)

    def test_independent_row_cursor_private_resume(self):
        witness = data(3, 2)
        values = parameters(witness)
        session = verify.runtime.Replay(self.folder / "state", {"control": 1})
        rows = iter(verify.construction.rows(*values))

        def interrupted():
            yield next(rows)
            raise RuntimeError("controlled interruption")

        with self.assertRaises(RuntimeError):
            verify.independent.check_rows(3, 2, F(10), interrupted(), session)
        retained = session.stage("verification")
        self.assertEqual(retained["next_k"], 2)
        retained["covers_hex"][0] = "bad"
        self.assertNotEqual(retained, session.stage("verification"))
        session.close()
        resumed = verify.runtime.Replay(self.folder / "state", {"control": 1})
        actual = verify.independent.check_rows(
            3, 2, F(10), verify.construction.rows(*values, start=2), resumed
        )
        resumed.finish()
        resumed.close()
        self.assertTrue(actual["accepted"])
        fresh = verify.runtime.Replay(self.folder / "state", {"control": 1})
        self.assertIsNone(fresh.stage("verification"))
        fresh.close()

    def test_checkpoint_identity_checksum_and_single_owner(self):
        path = self.folder / "state"
        first = verify.runtime.Replay(path, {"input": 1})
        first.save("control", {"next_k": 2})
        with self.assertRaises(ValueError):
            verify.runtime.Replay(path, {"input": 1})
        first.close()
        with self.assertRaises(ValueError):
            verify.runtime.Replay(path, {"input": 2})
        latest = path / "latest.json"
        value = json.loads(latest.read_text())
        value["stages"]["control"]["next_k"] = 3
        latest.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaises(ValueError):
            verify.runtime.Replay(path, {"input": 1})

    def test_completed_replay_can_switch_modes_but_partial_identity_cannot(self):
        path = self.folder / "modes"
        for mode in ("default", "export", "check_array"):
            replay = verify.runtime.Replay(path, {"mode": mode})
            self.assertIsNone(replay.stage("verification"))
            replay.save("verification", {"next_k": 4})
            replay.finish()
            replay.close()
        partial = verify.runtime.Replay(path, {"mode": "partial"})
        partial.save("verification", {"next_k": 2})
        partial.close()
        with self.assertRaises(ValueError):
            verify.runtime.Replay(path, {"mode": "another_input"})

    def test_tiny_default_export_actual_array_sequence_in_same_state_directory(self):
        witness = data(2)
        explicit = document(witness)
        content = (json.dumps(explicit, separators=(",", ":")) + "\n").encode()
        witness["provenance"]["declared_dense_sha256"] = hashlib.sha256(
            content
        ).hexdigest()
        path = self.write(witness, "witness.json")
        state, output = self.folder / "sequence", self.folder / "export.json"
        # A deliberately weaker declaration makes the tiny algebraic control
        # acceptable; the immutable flagship stronger declaration is unchanged.
        with patch.object(verify, "BOUND", F(10)):
            first = verify.replay_witness(path, state)
            exported = verify.replay_witness(path, state, output)
            checked = verify.check_array(output, path, state)
        self.assertTrue(
            first["accepted"] and exported["accepted"] and checked["accepted"]
        )
        self.assertEqual(output.read_bytes(), content)
        for key in ("a", "b", "ab", "energy", "cover_count"):
            self.assertEqual(first[key], checked[key])

    def test_independent_checker_imports_no_construction_module(self):
        source = (PACKAGE / "independent.py").read_text(encoding="utf-8")
        self.assertNotIn("import construction", source)
        self.assertNotIn("import numpy", source)
        self.assertNotIn("import scipy", source)
        self.assertNotIn("import ijson", source)


if __name__ == "__main__":
    unittest.main()
