"""Check the archived AJ01 instruction candidate's published byte contract."""

from pathlib import Path
import subprocess
import sys
import unittest


class AJ01InstructionCandidateTests(unittest.TestCase):
    def test_preserved_instruction_candidate(self):
        root = Path(__file__).resolve().parents[1]
        checker = (
            root / "capabilities" / "askjamie-aj01-resume-representative"
            / "docs" / "thread-closeout-instruction-prompt-2025-11-16" / "validate.py"
        )
        result = subprocess.run(
            [sys.executable, str(checker)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
