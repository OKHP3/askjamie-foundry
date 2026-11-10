"""Check that the candidate Replit entries point to the canonical skills."""

import hashlib
from pathlib import Path
import re
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
                entry = ROOT / "capabilities" / name / "adapters" / "replit" / name / "SKILL.md"
                config, body = metadata(entry)
                target = f"capabilities/{name}/skills/{name}/SKILL.md"
                self.assertEqual(config["name"], name)
                self.assertEqual(config["name"], entry.parent.name)
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
                entry = ROOT / "capabilities" / name / "adapters" / "replit" / name / "SKILL.md"
                config, _ = metadata(entry)
                self.assertEqual(
                    config["metadata"]["status"], "unverified-host-activation-candidate"
                )

    def test_buyer_router_pins_the_current_canonical_procedure(self):
        entry = (
            ROOT / "capabilities/professional-portfolio/adapters/replit"
            / "aj02-buyer-reply/SKILL.md"
        )
        config, body = metadata(entry)
        self.assertEqual(config["name"], "aj02-buyer-reply")
        self.assertEqual(config["metadata"]["status"], "isolated-routing-experiment")
        target = "capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md"
        self.assertIn(target, body)

        # Check the canonical LF content even when this test runs in a CRLF
        # checkout. The router itself checks raw bytes and will reject CRLF.
        canonical = (ROOT / target).read_bytes().replace(b"\r\n", b"\n")
        self.assertNotIn(b"\r", canonical)
        pins = re.findall(r"SHA-256\s+([0-9a-f]{64})", body)
        self.assertEqual(pins, [hashlib.sha256(canonical).hexdigest()])
        self.assertIn("stop without drafting", body)


if __name__ == "__main__":
    unittest.main()
