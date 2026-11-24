import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("checker", Path(__file__).with_name("check-technology-versions.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ReleaseEvidenceTests(unittest.TestCase):
    def test_missing_release_is_incomplete(self):
        with self.assertRaises(ValueError):
            checker.latest_release("Service unavailable", r"Release (\d+\.\d+) \(")

    def test_python_prerelease_is_not_stable(self):
        text = "<a>Python 3.15.0rc1</a><a>Python 3.11.16</a><a>Python 3.14.7</a>"
        self.assertEqual(checker.latest_release(text, r">Python (3\.\d+\.\d+)</a>"), "3.14.7")

    def test_nixos_current_release_notes_format(self):
        self.assertEqual(checker.latest_release("Release 25.11 (old) Release 26.05 (current)", r"Release (\d+\.\d+) \("), "26.05")


if __name__ == "__main__":
    unittest.main()
