"""Standard-library controls for the recovered certificate's two-checker wrapper."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "certificates" / "two_sided_recovery"
SPEC = importlib.util.spec_from_file_location(
    "recovered_public_wrapper", PACKAGE / "verify.py"
)
assert SPEC is not None and SPEC.loader is not None
wrapper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wrapper)


def control() -> dict[str, object]:
    return {
        "format_version": "mathis.research.sidon.two_sided_smoothing_certificate.v1",
        "block_size": 1,
        "window_length": 1,
        "declared_bound": "2",
        "kernels": [["1"]],
        "mixing": ["1"],
        "left_boundary": [["1"]],
        "right_boundary": "ones",
    }


class RecoveryPublicTests(unittest.TestCase):
    def run_cli(self, document=None, raw=None, script=None):
        with tempfile.TemporaryDirectory(prefix="sidon-recovery-public-") as temp:
            command = [sys.executable, "-I", "-S", str(script or PACKAGE / "verify.py")]
            if document is not None or raw is not None:
                path = Path(temp) / "control.json"
                path.write_text(
                    raw if raw is not None else json.dumps(document), encoding="utf-8"
                )
                command.append(str(path))
            result = subprocess.run(
                command, cwd=temp, text=True, capture_output=True, timeout=120
            )
            self.assertTrue(result.stdout, result.stderr)
            return result.returncode, json.loads(result.stdout)

    def test_bundled_winner_from_isolated_unrelated_directory(self):
        code, output = self.run_cli()
        self.assertEqual(code, 0, output)
        self.assertTrue(output["accepted"])
        self.assertTrue(output["agreement"])
        self.assertTrue(output["manifest_checked"])
        self.assertTrue(output["independent"]["beats_target"])
        self.assertEqual(output["independent"]["covers"]["total"], 16386)
        self.assertEqual(
            output["independent"]["declared_bound"], "188561854127/200000000000"
        )

    def test_feasible_control_is_not_a_benchmark_win(self):
        code, output = self.run_cli(control())
        self.assertEqual(code, 1)
        self.assertTrue(output["research"]["checks_passed"])
        self.assertTrue(output["independent"]["accepted_feasible"])
        self.assertFalse(output["independent"]["beats_target"])

    def test_nonpositive_bound_strict_equality_and_cover_failure(self):
        for changes in (
            {"declared_bound": "0"},
            {"declared_bound": "-2"},
            {"declared_bound": "1"},
            {"left_boundary": [["0"]]},
        ):
            with self.subTest(changes=changes):
                document = control()
                document.update(changes)
                code, output = self.run_cli(document)
                self.assertEqual(code, 1, output)
                self.assertFalse(output["accepted"])

    def test_malformed_dimensions_and_explicit_independent_scope(self):
        for changes in (
            {"block_size": 0},
            {"window_length": True},
            {"left_boundary": [[]]},
            {"kernels": [["1/2"]]},
            {"right_boundary": [["1"]]},
            {"mixing": ["1/2"]},
        ):
            with self.subTest(changes=changes):
                document = control()
                document.update(changes)
                code, output = self.run_cli(document)
                self.assertEqual(code, 2, output)
                self.assertIn("input_error", output)

    def test_invalid_and_duplicate_json(self):
        for raw in ("{", '{"block_size":1,"block_size":2}', '{"x":NaN}'):
            with self.subTest(raw=raw):
                self.assertEqual(self.run_cli(raw=raw)[0], 2)

    def test_checker_disagreement_rejects(self):
        with tempfile.TemporaryDirectory(prefix="sidon-disagreement-") as temp:
            path = Path(temp) / "control.json"
            path.write_text(json.dumps(control()), encoding="utf-8")
            direct = wrapper.independent.verify_certificate(path)
            direct["b"] = "2"
            with patch.object(
                wrapper.independent, "verify_certificate", return_value=direct
            ):
                result = wrapper.check_one(path)
            self.assertFalse(result["agreement"])
            self.assertFalse(result["accepted"])
            self.assertIn(
                "independent checking implementations disagree", result["failures"]
            )

    def test_manifest_tamper_and_expected_results_mismatch(self):
        for target_name, content in (
            ("verify.py", "\n#tamper\n"),
            ("EXPECTED_RESULTS.json", "{}"),
            ("EXPECTED_RESULTS.json", "valid-but-wrong"),
        ):
            with (
                self.subTest(target=target_name),
                tempfile.TemporaryDirectory(prefix="sidon-package-") as temp,
            ):
                copied = Path(temp) / "package"
                shutil.copytree(PACKAGE, copied)
                target = copied / target_name
                if target_name == "verify.py":
                    target.write_text(
                        target.read_text(encoding="utf-8") + content, encoding="utf-8"
                    )
                else:
                    if content == "valid-but-wrong":
                        expected = json.loads(target.read_text(encoding="utf-8"))
                        expected["independent"]["b"] = "2"
                        content = json.dumps(expected)
                    target.write_text(content, encoding="utf-8")
                    manifest_path = copied / "MANIFEST.json"
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    for member in manifest["files"]:
                        if member["path"] == target_name:
                            data = target.read_bytes()
                            member.update(
                                bytes=len(data), sha256=hashlib.sha256(data).hexdigest()
                            )
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                code, output = self.run_cli(script=copied / "verify.py")
                self.assertEqual(code, 2, output)
                self.assertIn("input_error", output)

    def test_manifest_unsafe_duplicate_and_missing_members(self):
        original = json.loads((PACKAGE / "MANIFEST.json").read_text(encoding="utf-8"))
        for change in ("unsafe", "duplicate", "missing"):
            with (
                self.subTest(change=change),
                tempfile.TemporaryDirectory(prefix="sidon-manifest-") as temp,
            ):
                copied = Path(temp) / "package"
                shutil.copytree(PACKAGE, copied)
                manifest = json.loads(json.dumps(original))
                if change == "unsafe":
                    manifest["files"][0]["path"] = "../outside"
                elif change == "duplicate":
                    manifest["files"].append(manifest["files"][0])
                else:
                    manifest["files"] = []
                (copied / "MANIFEST.json").write_text(
                    json.dumps(manifest), encoding="utf-8"
                )
                self.assertEqual(self.run_cli(script=copied / "verify.py")[0], 2)

    def test_missing_checker_module_is_controlled_integrity_error(self):
        with tempfile.TemporaryDirectory(prefix="sidon-missing-checker-") as temp:
            copied = Path(temp) / "package"
            shutil.copytree(PACKAGE, copied)
            (copied / "independent.py").unlink()
            code, output = self.run_cli(script=copied / "verify.py")
            self.assertEqual(code, 2, output)
            self.assertIn("checker import failed", output["input_error"])


if __name__ == "__main__":
    unittest.main()
