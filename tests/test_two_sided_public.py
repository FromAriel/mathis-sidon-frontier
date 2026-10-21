"""Standard-library acceptance and rejection controls for the portable checker."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "certificates" / "two_sided"
sys.path.insert(0, str(CHECKER))
from smoothing_verify import (  # noqa: E402
    TwoSidedSmoothingCertificate,
    build_uniform_certificate,
    parse_two_sided_certificate,
    verify_certificate,
    verify_two_sided_certificate,
)


def payload() -> dict:
    return {
        "format_version": "mathis.research.sidon.two_sided_smoothing_certificate.v1",
        "block_size": 1,
        "window_length": 1,
        "declared_bound": "2",
        "mixing": ["1"],
        "kernels": [["1"]],
        "left_boundary": [["1"]],
        "right_boundary": "ones",
    }


class PublicCheckerTests(unittest.TestCase):
    def check(self, document: dict):
        return verify_two_sided_certificate(parse_two_sided_certificate(document))

    def run_cli(self, document: dict):
        with tempfile.TemporaryDirectory(prefix="sidon-certificate-") as directory:
            certificate = Path(directory) / "control.json"
            certificate.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-I", "-S", str(CHECKER / "verify.py"), str(certificate)],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
            return result.returncode, json.loads(result.stdout)

    def test_positive_control_and_exact_strictness(self):
        self.assertTrue(self.check(payload()).checks_passed)
        document = payload()
        document["declared_bound"] = "1"
        self.assertFalse(self.check(document).checks_passed)

    def test_nonpositive_bounds_parser_typed_and_cli(self):
        positive = parse_two_sided_certificate(payload())
        for bound in ("0", "-2"):
            with self.subTest(bound=bound):
                document = payload()
                document["declared_bound"] = bound
                with self.assertRaises(ValueError):
                    parse_two_sided_certificate(document)
                direct = verify_two_sided_certificate(
                    replace(positive, declared_bound=Fraction(bound))
                )
                self.assertFalse(direct.checks_passed)
                self.assertFalse(direct.bound_holds)
                code, output = self.run_cli(document)
                self.assertEqual(code, 1)
                self.assertFalse(output["checks_passed"])

    def test_both_covering_ends(self):
        for side in ("left_boundary", "right_boundary"):
            document = payload()
            document[side] = [["0"]]
            result = self.check(document)
            self.assertFalse(result.checks_passed)
            self.assertTrue(any("covering" in failure for failure in result.failures))

    def test_reversal_is_required(self):
        document = payload()
        document.update(
            block_size=2,
            kernels=[["1/4", "3/4"]],
            left_boundary=[["1", "1"]],
            right_boundary=[["0", "2"]],
        )
        self.assertFalse(self.check(document).checks_passed)

    def test_malformed_rows_and_dimensions(self):
        for patch in (
            {"kernels": ["1"]},
            {"left_boundary": ["1"]},
            {"right_boundary": ["1"]},
            {"left_boundary": [[]]},
            {"mixing": []},
            {"block_size": 0},
            {"window_length": 0},
        ):
            document = payload()
            document.update(patch)
            with self.subTest(patch=patch), self.assertRaises((ValueError, TypeError)):
                parse_two_sided_certificate(document)

    def test_normalization_and_structural_last_row(self):
        document = payload()
        document["kernels"] = [["1/2"]]
        result = self.check(document)
        self.assertFalse(result.checks_passed)
        self.assertTrue(any("q=1" in failure for failure in result.failures))
        document = payload()
        document["mixing"] = ["1/2"]
        self.assertFalse(self.check(document).checks_passed)

    def test_joint_mixture_and_signed_boundaries(self):
        document = payload()
        document.update(
            mixing=["1/2", "1/2"],
            kernels=[["1"], ["1"]],
            left_boundary=[["0"], ["2"]],
            right_boundary=[["2"], ["0"]],
        )
        result = self.check(document)
        self.assertTrue(result.checks_passed)
        self.assertEqual(result.gamma_squared, 3)
        document.update(
            mixing=["1/3", "1/3", "1/3"],
            kernels=[["1"], ["1"], ["1"]],
            left_boundary=[["-1"], ["1"], ["3"]],
            right_boundary=[["-1"], ["1"], ["3"]],
            declared_bound="3",
        )
        self.assertTrue(self.check(document).checks_passed)

    def test_symmetric_formula_equivalence(self):
        old = replace(build_uniform_certificate(), declared_bound=Fraction(2))
        new = TwoSidedSmoothingCertificate(
            mixing=old.mixing,
            kernels=old.kernels,
            left_boundary=old.boundary,
            right_boundary=old.boundary,
            window_length=old.window_length,
            block_size=old.block_size,
            declared_bound=old.declared_bound,
        )
        first, second = verify_certificate(old), verify_two_sided_certificate(new)
        self.assertEqual(first.energy_constant, second.energy_constant)
        self.assertEqual(first.boundary_constant, second.boundary_constant)
        self.assertEqual(first.gamma_squared, second.gamma_squared)

    def test_cli_acceptance_rejection_and_input_error(self):
        self.assertEqual(self.run_cli(payload())[0], 0)
        document = payload()
        document["left_boundary"] = [["-1"]]
        code, output = self.run_cli(document)
        self.assertEqual(code, 1)
        self.assertFalse(output["checks_passed"])
        document["block_size"] = 0
        self.assertEqual(self.run_cli(document)[0], 2)

    def test_negative_energy_has_no_square_root_failure(self):
        document = payload()
        document.update(left_boundary=[["0"]], right_boundary=[["0"]])
        result = self.check(document)
        self.assertFalse(result.checks_passed)
        self.assertLess(result.gamma_squared, 0)
        self.assertIsNone(result.to_dict()["gamma_float_diagnostic_only"])


if __name__ == "__main__":
    unittest.main()
