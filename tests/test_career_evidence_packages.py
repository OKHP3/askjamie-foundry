"""Structural release gates only; these tests do not execute an agent skill."""
import hashlib
import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capabilities/resume-representative"
NAMES = ("okhp3-work-search-evidence", "okhp3-career-artifact-audit")


class CareerEvidencePackageTests(unittest.TestCase):
    def test_exact_package_inventory_and_metadata(self):
        found = [CAP / "skills" / n for n in NAMES if (CAP / "skills" / n / "SKILL.md").is_file()]
        self.assertEqual(len(NAMES), len(found), "Missing or zero target packages must fail.")
        for package in found:
            with self.subTest(package=package.name):
                text = (package / "SKILL.md").read_text(encoding="utf-8")
                parts = text.split("---", 2)
                self.assertEqual("", parts[0])
                meta = yaml.safe_load(parts[1])
                self.assertEqual(package.name, meta["name"])
                self.assertRegex(meta["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(meta["name"]), 36)
                self.assertTrue(0 < len(meta["description"]) <= 1024)
                self.assertEqual("MIT", meta["license"])
                self.assertEqual("1.0.0", meta["metadata"]["version"])
                for field in ("author", "version", "category", "origin", "homepage", "author-github", "in_scope", "out_of_scope"):
                    self.assertIsInstance(meta["metadata"][field], str)
                    self.assertTrue(meta["metadata"][field])
                self.assertLess(len(parts[2].splitlines()), 500)
                self.assertTrue((package / "LICENSE.md").is_file())
                for resource in package.rglob("*"):
                    if resource.is_file():
                        self.assertLessEqual(len(resource.relative_to(ROOT).as_posix()), 180)
                        self.assertTrue(all(len(p) <= 64 for p in resource.relative_to(ROOT).parts))

    def test_relative_resources_and_json_are_present(self):
        for name in NAMES:
            package = CAP / "skills" / name
            for source in package.rglob("*.md"):
                text = source.read_text(encoding="utf-8")
                self.assertNotIn("\u2014", text)
                for target in re.findall(r"\]\(([^)]+)\)", text):
                    if target.startswith(("http://", "https://", "#")):
                        continue
                    relative = target.split("#", 1)[0]
                    actual = (source.parent / relative).resolve()
                    self.assertTrue(actual.is_relative_to(package.resolve()), target)
                    self.assertTrue(actual.is_file(), target)
            for source in package.rglob("*.json"):
                json.loads(source.read_text(encoding="utf-8"))

    def test_development_cases_and_truthful_evidence_status(self):
        for name in NAMES:
            data = json.loads((CAP / "skills" / name / "evals/evals.json").read_text(encoding="utf-8"))
            self.assertEqual(name, data["skill_name"])
            self.assertEqual("1.0.0", data["skill_version"])
            self.assertEqual("not-run", data["evaluation_status"])
            self.assertEqual("external-required", data["holdout"]["status"])
            self.assertIs(data["holdout"]["holdout_seen"], True)
            self.assertEqual([], data["holdout"]["cases"])
            self.assertEqual(0, data["acceptance"]["critical_failures_allowed"])
            self.assertGreaterEqual(len(data["evals"]), 6)
            ids = [case["id"] for case in data["evals"]]
            self.assertEqual(len(ids), len(set(ids)))
            for case in data["evals"]:
                self.assertEqual("development", case["partition"])
                self.assertTrue(case["prompt"])
                self.assertTrue(case["fixture"])
                self.assertGreaterEqual(len(case["expectations"]), 3)
                self.assertTrue(all(e["critical"] and e["text"] for e in case["expectations"]))

    def test_frozen_artifact_hashes(self):
        record = json.loads((CAP / "docs/career-skill-review/release.json").read_text(encoding="utf-8"))
        self.assertEqual("analytical", record["evaluation_status"])
        self.assertEqual(set(NAMES), {p["name"] for p in record["packages"]})
        expected = {p.relative_to(ROOT).as_posix()
                    for name in NAMES for p in (CAP / "skills" / name).rglob("*") if p.is_file()}
        expected.add("capabilities/resume-representative/docs/career-workflow-skills.md")
        self.assertEqual(expected, set(record["artifact_hashes"]))
        for rel, digest in record["artifact_hashes"].items():
            self.assertEqual(digest, hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), rel)
        serialized = json.dumps(record)
        self.assertNotIn("production-ready", serialized)

    def test_populated_audit_example_preserves_observation_boundaries(self):
        package = CAP / "skills/okhp3-career-artifact-audit"
        example = json.loads((package / "assets/audit-example.json").read_text(encoding="utf-8"))
        template = json.loads((package / "assets/audit-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(template), set(example))
        self.assertEqual(2, example["coverage"]["checked_reference_count"])
        self.assertEqual("unverified", example["sync_status"])
        self.assertEqual({"exact-id", "unavailable"}, {m["mapping_status"] for m in example["mappings"]})
        ids = {item["item_key"] for item in example["items"]}
        self.assertTrue(all(m["item_key"] in ids for m in example["mappings"]))
        self.assertTrue(all(item["observations"]["local_content"]["status"] == "unchecked" for item in example["items"]))
        self.assertEqual("not-saved", example["report_storage"]["result"])
        self.assertEqual("existing-file", example["report_storage"]["collision_status"])
        self.assertIsNone(example["report_storage"]["create_guard"])

    def test_discovery_design_is_not_reported_as_measured_activation(self):
        for name in NAMES:
            data = json.loads((CAP / "skills" / name / "evals/discovery.json").read_text(encoding="utf-8"))
            self.assertEqual(name, data["skill_name"])
            self.assertEqual("not-run", data["evaluation_status"])
            self.assertEqual("unverified", data["automatic_activation"])
            self.assertIsNone(data["precision"])
            self.assertIsNone(data["recall"])
            self.assertEqual(20, len(data["queries"]))
            self.assertEqual(20, len({q["id"] for q in data["queries"]}))
            self.assertEqual({True, False}, {q["expected_activate"] for q in data["queries"]})
