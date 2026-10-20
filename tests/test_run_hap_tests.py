"""Unit tests for the fixed-command HAP test orchestrator."""
from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from scripts.run_hap_tests import build_steps, run_step


class HAPTestRunnerTests(unittest.TestCase):
    def test_only_fixed_repository_checks_are_configured(self) -> None:
        steps = build_steps("/python")
        self.assertEqual(
            [step["name"] for step in steps],
            ["evidence_metadata_validation", "python_unit_tests"],
        )
        self.assertTrue(all(step["command"][0] == "/python" for step in steps))
        self.assertTrue(all(isinstance(step["command"], list) for step in steps))

    @patch("scripts.run_hap_tests.subprocess.run")
    def test_successful_step_is_pass(self, mocked_run) -> None:
        mocked_run.return_value = subprocess.CompletedProcess(
            args=["python", "check.py"], returncode=0, stdout="ok\n", stderr=""
        )
        result = run_step(
            {"name": "test", "command": ["python", "check.py"]},
            timeout_seconds=10,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["exit_code"], 0)
        self.assertFalse(mocked_run.call_args.kwargs["shell"])

    @patch("scripts.run_hap_tests.subprocess.run")
    def test_nonzero_exit_is_fail(self, mocked_run) -> None:
        mocked_run.return_value = subprocess.CompletedProcess(
            args=["python", "check.py"], returncode=3, stdout="", stderr="failed"
        )
        result = run_step(
            {"name": "test", "command": ["python", "check.py"]},
            timeout_seconds=10,
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["exit_code"], 3)

    @patch("scripts.run_hap_tests.subprocess.run")
    def test_timeout_is_not_pass(self, mocked_run) -> None:
        mocked_run.side_effect = subprocess.TimeoutExpired(
            cmd=["python", "check.py"], timeout=1, output="partial", stderr=""
        )
        result = run_step(
            {"name": "test", "command": ["python", "check.py"]},
            timeout_seconds=1,
        )
        self.assertEqual(result["status"], "TIMEOUT")
        self.assertIsNone(result["exit_code"])


if __name__ == "__main__":
    unittest.main()
