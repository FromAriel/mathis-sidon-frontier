"""Isolated standard-library controls for the finite-grid public package."""

from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "certificates" / "finite_grid"
SPEC = importlib.util.spec_from_file_location("finite_grid_public_wrapper", PACKAGE / "verify.py")
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


def witness_and_array(n=3, depth=2, bits=24, p=12):
    """Literal fractions, direct recurrence sums and original-box repair."""
    d, count, size, scale = 2 * n - 1, n * depth, 2 * n * depth, 1 << p
    lo, hi, q = [], [], []
    for t in range(count):
        if t == 0:
            left = right = n * n * (1 << bits)
        else:
            left = 2 * sum(lo[max(0, t - n + 1) : t])
            right = 2 * sum(hi[max(0, t - n + 1) : t])
            if t >= n:
                left += lo[t - n]
                right += hi[t - n]
        lo.append(left // d)
        hi.append(-((-right) // d))
        midpoint = F(lo[-1] + hi[-1], 1 << (bits + 1 - p))
        floor = midpoint.numerator // midpoint.denominator
        q.append(min((floor, floor + 1), key=lambda x: (abs(x - midpoint), x % 2)))
    weights = [F(4 * k**3, n**4) if k < n else F(d, n * n) for k in range(1, n + 1)]
    rows = []
    for k in range(1, n + 1):
        rows.append(
            [
                sum(
                    (
                        F(q[(j - n + k) // 2 - a], k * scale)
                        for a in range(k)
                        if (j - n + k) // 2 >= a
                    ),
                    F(0),
                )
                for j in range(size)
            ]
        )

    def cover(row):
        return sum(
            (
                weights[k - 1]
                * sum(
                    (rows[k - 1][row + i] if row + i < size else F(1) for i in range(n - k, n + k)),
                    F(0),
                )
                / (2 * k)
                for k in range(1, n + 1)
            ),
            F(0),
        )

    for row in range(size - 1, -1, -1):
        rows[-1][row] += 2 * n * (1 - cover(row)) / weights[-1]
    assert all(cover(row) == 1 for row in range(size + 1))
    full_den = n * d * scale
    full = [value * full_den for value in rows[-1]]
    assert all(value.denominator == 1 for value in full)
    value = sum(
        (
            weight * sum((x * x for x in row), F(0))
            for weight, row in zip(weights, rows, strict=True)
        ),
        F(0),
    )
    a = F(4, 3) - F(1, 3 * n * n)
    b = 1 + value / n - 2 * depth

    def endpoint_hash(values):
        return hashlib.sha256("".join(format(x, "x") + "\n" for x in values).encode()).hexdigest()

    witness = {
        "format_version": verify.reconstruction.FORMAT,
        "n": n,
        "L": depth,
        "s": bits,
        "p": p,
        "target": "10",
        "coarse_y_hex": [format(x, "x") for x in q],
        "full_hex": [format(x.numerator, "x") for x in full],
        "full_den_hex": format(full_den, "x"),
        "V": str(value),
        "a": str(a),
        "b": str(b),
        "ab": str(a * b),
        "lower_sha256": endpoint_hash(lo),
        "upper_sha256": endpoint_hash(hi),
        "source_bindings": {name: "0" * 64 for name in verify.reconstruction.SOURCE_FIELDS},
    }
    dense = {
        "format_version": "mathis.research.sidon.smoothing_certificate.v1",
        "block_size": 2 * n,
        "window_length": depth,
        "declared_bound": "10",
        "mixing": list(map(str, weights)),
        "kernels": [
            [str(F(1, 2 * k)) if n - k <= i < n + k else "0" for i in range(2 * n)]
            for k in range(1, n + 1)
        ],
        "boundary": [list(map(str, row)) for row in rows],
    }
    return witness, dense


class FiniteGridPublicTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "tmp" / "finite_grid_public_tests"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)

    def write(self, value, name="fixture.json"):
        path = self.folder / name
        path.write_text(json.dumps(value, separators=(",", ":")) + "\n", encoding="utf-8")
        return path

    def test_literal_original_covers_and_energy(self):
        for n in (1, 2, 3, 8, 16):
            for depth in (1, 2):
                with self.subTest(n=n, L=depth):
                    witness, dense = witness_and_array(n, depth)
                    path = self.write(witness)
                    result = verify.reconstruction.verify(path)
                    rows = [[F(x) for x in row] for row in dense["boundary"]]
                    mixing = list(map(F, dense["mixing"]))
                    energy = sum(
                        (
                            weight * sum((x * x for x in row), F(0))
                            for weight, row in zip(mixing, rows, strict=True)
                        ),
                        F(0),
                    )
                    self.assertEqual(F(result["V"]), energy)
                    self.assertEqual(F(result["b"]), 1 + energy / n - 2 * depth)
                    self.assertTrue(result["accepted"])
                    self.assertTrue(result["all_covers_exactly_one"])
                    self.assertEqual(result["cover_count"], 2 * n * depth + 1)

    def test_approved_precisions_replay_small_exact_intervals(self):
        for s, p in ((128, 80), (256, 128)):
            with self.subTest(s=s, p=p):
                witness, _ = witness_and_array(3, 2, s, p)
                self.assertTrue(verify.reconstruction.verify(self.write(witness))["accepted"])

    def test_compact_rejections(self):
        original, _ = witness_and_array()
        for mutation in (
            "q",
            "first_full",
            "late_full",
            "lower",
            "upper",
            "V",
            "a",
            "b",
            "ab",
            "denominator",
            "schema",
            "bool",
            "provenance",
            "hex",
            "cap",
        ):
            with self.subTest(mutation=mutation):
                value = copy.deepcopy(original)
                if mutation == "q":
                    value["coarse_y_hex"][-1] = format(int(value["coarse_y_hex"][-1], 16) + 1, "x")
                elif mutation in ("first_full", "late_full"):
                    index = 0 if mutation == "first_full" else -1
                    value["full_hex"][index] = format(int(value["full_hex"][index], 16) + 1, "x")
                elif mutation in ("lower", "upper"):
                    value[mutation + "_sha256"] = "f" * 64
                elif mutation in ("a", "b", "ab", "V"):
                    value[mutation] = str(F(value[mutation]) + 1)
                elif mutation == "denominator":
                    value["full_den_hex"] = "0"
                elif mutation == "schema":
                    value["accepted"] = True
                elif mutation == "bool":
                    value["n"] = True
                elif mutation == "provenance":
                    value["source_bindings"] = {"private_path": "0" * 64}
                elif mutation == "hex":
                    value["full_hex"][0] = "00"
                else:
                    value["full_hex"][0] = format(1 << 4096, "x")
                with self.assertRaises((ValueError, ArithmeticError)):
                    verify.reconstruction.verify(self.write(value))

    def test_duplicate_inexact_and_trailing_json_are_rejected(self):
        witness, _ = witness_and_array()
        raw = json.dumps(witness)
        for text in (
            raw.replace('"n": 3', '"n": 3, "n": 3'),
            raw.replace('"n": 3', '"n": 3.0'),
            raw.replace('"n": 3', '"n": NaN'),
            raw + "{}",
        ):
            with self.subTest(text=text[:40]):
                path = self.folder / "invalid.json"
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    verify.reconstruction.verify(path)

    def test_ties_even_and_failed_target(self):
        self.assertEqual(
            [verify.reconstruction._nearest_even(x, 2) for x in (1, 3, 5, 7)],
            [0, 2, 2, 4],
        )
        witness, _ = witness_and_array()
        witness["target"] = "1/2"
        result = verify.reconstruction.verify(self.write(witness))
        self.assertTrue(result["positive_b"])
        self.assertFalse(result["accepted"])

    def test_private_resume_and_callback_isolation(self):
        witness, _ = witness_and_array(8)
        path = self.write(witness)
        expected = verify.reconstruction.verify(path)
        states = []

        class Interrupted(Exception):
            pass

        def stop(state):
            states.append(copy.deepcopy(state))
            if state["next_k"] == 4:
                raise Interrupted

        with self.assertRaises(Interrupted):
            verify.reconstruction.verify(path, progress=stop)
        saved = copy.deepcopy(states[-1])
        self.assertEqual(verify.reconstruction.verify(path, state=saved), expected)
        self.assertEqual(saved, states[-1])

        def poison(state):
            state["flat_hex"][:] = ["0"] * len(state["flat_hex"])
            state["wu_hex"][:] = ["0"] * len(state["wu_hex"])
            state["energy_hex"] = "0"

        self.assertEqual(verify.reconstruction.verify(path, progress=poison), expected)
        witness["source_bindings"]["research_core_sha256"] = "1" * 64
        with self.assertRaisesRegex(ValueError, "checkpoint identity"):
            verify.reconstruction.verify(self.write(witness), state=saved)

    def test_runtime_private_stage_and_completed_runs_start_fresh(self):
        state_dir = self.folder / "checkpoint"
        first = verify.runtime.Replay(state_dir, {"input": "first"})
        source = {"next_k": 2, "values": [1]}
        first.save("compact", source)
        source["values"][0] = 9
        exposed = first.stage("compact")
        exposed["values"][0] = 7
        self.assertEqual(first.stage("compact")["values"], [1])
        first.finish()
        first.close()
        second = verify.runtime.Replay(state_dir, {"input": "second"})
        self.assertIsNone(second.stage("compact"))
        self.assertFalse(second.state["complete"])
        second.close()

    def test_runtime_lock_and_invalid_checkpoint_fail_closed(self):
        state_dir = self.folder / "locks"
        first = verify.runtime.Replay(state_dir, {"input": "a"})
        first.save("compact", {"next_k": 2})
        with self.assertRaisesRegex(ValueError, "another process"):
            verify.runtime.Replay(state_dir, {"input": "a"})
        first.close()
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            verify.runtime.Replay(state_dir, {"input": "changed"})
        latest = state_dir / "latest.json"
        saved = latest.read_bytes()
        latest.write_text("{", encoding="utf-8")
        with self.assertRaises(ValueError):
            verify.runtime.Replay(state_dir, {"input": "a"})
        latest.write_bytes(saved)
        recovered = verify.runtime.Replay(state_dir, {"input": "a"})
        self.assertEqual(recovered.stage("compact")["next_k"], 2)
        recovered.close()

    def test_completed_wrapper_replays_fresh_arithmetic(self):
        witness, _ = witness_and_array(3)
        path = self.write(witness)
        directory = self.folder / "repeat"
        original = verify.reconstruction.verify
        supplied_states = []

        def record(path, **kwargs):
            supplied_states.append(kwargs["state"])
            return original(path, **kwargs)

        with patch.object(verify.reconstruction, "verify", side_effect=record):
            first = verify.replay_witness(path, directory)
            second = verify.replay_witness(path, directory)
        self.assertEqual(first, second)
        self.assertEqual(supplied_states, [None, None])

    def test_gzip_export_and_independent_actual_arrays(self):
        for n in (1, 2, 3, 8, 16):
            with self.subTest(n=n):
                witness, dense = witness_and_array(n)
                path = self.write(witness)
                output = self.folder / ("array_" + str(n) + ".json.gz")
                state_dir = self.folder / ("export_" + str(n))
                compact = verify.replay_witness(path, state_dir, output)
                actual = json.loads(gzip.decompress(output.read_bytes()))
                self.assertEqual(actual, dense)
                array = verify.check_array(output, path)
                self.assertTrue(array["accepted"])
                for key in (
                    "V",
                    "a",
                    "b",
                    "ab",
                    "cover_count",
                    "all_covers_exactly_one",
                ):
                    self.assertEqual(array[key], compact[key])
                self.assertEqual(
                    compact["export"]["raw_sha256"],
                    hashlib.sha256(gzip.decompress(output.read_bytes())).hexdigest(),
                )
                with self.assertRaisesRegex(ValueError, "exists"):
                    verify.replay_witness(path, state_dir, output)

    def test_export_checkpoint_resume_and_caps(self):
        witness, dense = witness_and_array(3)
        exporter = verify.local_module("exporter")
        output = self.folder / "resume.json.gz"
        work = self.folder / "export_work"
        states = []

        class Interrupted(Exception):
            pass

        def stop(state):
            states.append(copy.deepcopy(state))
            if state["next_k"] == 2:
                raise Interrupted

        with self.assertRaises(Interrupted):
            exporter.export(witness, output, work, progress=stop)
        saved = copy.deepcopy(states[-1])
        receipt = exporter.export(witness, output, work, state=saved)
        self.assertEqual(saved, states[-1])
        self.assertEqual(json.loads(gzip.decompress(output.read_bytes())), dense)
        self.assertEqual(receipt["members"], 5)
        for keyword in ("compressed_cap", "raw_cap"):
            with self.subTest(cap=keyword), self.assertRaises(MemoryError):
                exporter.export(witness, self.folder / (keyword + ".gz"), work, **{keyword: 1})

    def test_array_rejection_preserves_independence(self):
        witness, dense = witness_and_array()
        path = self.write(witness)
        for mutation in ("late", "unused", "target", "kernel"):
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(dense)
                if mutation == "late":
                    data["boundary"][-1][-1] = "0"
                elif mutation == "unused":
                    data["boundary"][0][0] = "1"
                elif mutation == "target":
                    data["declared_bound"] = "11"
                else:
                    data["kernels"][0][0] = "1"
                output = self.folder / "bad.json.gz"
                output.write_bytes(gzip.compress(json.dumps(data).encode(), mtime=0))
                with self.assertRaises((ValueError, ArithmeticError)):
                    verify.check_array(output, path)

    def test_reference_comparison_cannot_supply_acceptance(self):
        witness, _ = witness_and_array()
        result = verify.reconstruction.verify(self.write(witness))
        verify.compare_reference(result, result)
        incorrect = dict(result, ab="0")
        with self.assertRaisesRegex(ValueError, "expected ab"):
            verify.compare_reference(result, incorrect)

    def test_manifest_inventory_identity_and_safe_paths(self):
        directory = self.folder / "inventory"
        directory.mkdir()
        names = (
            "WITNESS.json",
            "reconstruction.py",
            "runtime.py",
            "verify.py",
            "arraycheck.py",
            "exporter.py",
            "EXPECTED_RESULTS.json",
            "README.md",
            "PROOF.md",
            "PROVENANCE.md",
        )
        records = []
        for name in names:
            path = directory / name
            path.write_bytes(b"public input\n")
            records.append(
                {
                    "path": name,
                    "bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        manifest = directory / "MANIFEST.json"
        with patch.object(verify, "HERE", directory.resolve()):
            manifest.write_text(json.dumps({"files": records}), encoding="utf-8")
            verify.inventory()
            for mutation in ("duplicate", "escape", "hash", "missing"):
                with self.subTest(mutation=mutation):
                    changed = copy.deepcopy(records)
                    if mutation == "duplicate":
                        changed.append(changed[0])
                    elif mutation == "escape":
                        changed[0]["path"] = "../WITNESS.json"
                    elif mutation == "hash":
                        changed[0]["sha256"] = "0" * 64
                    else:
                        changed.pop()
                    manifest.write_text(json.dumps({"files": changed}), encoding="utf-8")
                    with self.assertRaises((ValueError, OSError)):
                        verify.inventory()

    def test_arithmetic_cap_rejects_before_large_integer_work(self):
        witness, _ = witness_and_array()
        witness["full_hex"][0] = "1" + "0" * (verify.reconstruction.INTEGER_CAP // 4)
        with self.assertRaisesRegex(ValueError, "oversized"):
            verify.reconstruction.verify(self.write(witness))

    def test_isolated_cli_and_parser_imports(self):
        witness, _ = witness_and_array()
        path = self.write(witness)
        # The manifest has its own inventory tests. Isolate a CLI invocation
        # without depending on the coordinator's not-yet-sealed manifest.
        command = (
            "import importlib.util,sys;"
            "s=importlib.util.spec_from_file_location('public_cli',"
            f"{str(PACKAGE / 'verify.py')!r});"
            "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
            "m.inventory=lambda:None;"
            f"raise SystemExit(m.main([{str(path)!r},'--no-checkpoint']))"
        )
        completed = subprocess.run(
            [sys.executable, "-I", "-S", "-c", command],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
        self.assertTrue(json.loads(completed.stdout)["accepted"])
        self.assertNotIn("ijson", completed.stderr)


if __name__ == "__main__":
    unittest.main()
