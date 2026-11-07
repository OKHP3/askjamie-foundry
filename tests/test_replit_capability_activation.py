"""Check that the candidate Replit entries point to the canonical skills."""

from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ("resume-representative", "professional-portfolio")


def metadata(path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Invalid skill frontmatter: {path}")
    return yaml.safe_load(parts[1]), parts[2]


class ReplitActivationContractTests(unittest.TestCase):
    def test_each_activation_resolves_to_its_canonical_procedure(self):
        for name in CAPABILITIES:
            with self.subTest(capability=name):
                entry = ROOT / "capabilities" / name / "adapters" / "replit" / "SKILL.md"
                config, body = metadata(entry)
                target = f"capabilities/{name}/skills/{name}/SKILL.md"
                self.assertEqual(config["name"], name)
                self.assertTrue(config["description"].strip())
                self.assertEqual(config["metadata"]["canonical_path"], target)
                self.assertIn(f"`{target}`", body)
                target_path = ROOT / target
                self.assertTrue(target_path.is_file(), target)
                canonical, _ = metadata(target_path)
                self.assertEqual(canonical["name"], name)

    def test_candidates_disclose_unverified_host_status(self):
        for name in CAPABILITIES:
            with self.subTest(capability=name):
                entry = ROOT / "capabilities" / name / "adapters" / "replit" / "SKILL.md"
                config, _ = metadata(entry)
                self.assertEqual(
                    config["metadata"]["status"], "unverified-host-activation-candidate"
                )


if __name__ == "__main__":
    unittest.main()
