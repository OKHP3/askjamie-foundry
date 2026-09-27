"""Evidence for portable exports, legacy preservation, and subtree privacy gates."""
import copy
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml
import jsonschema

from workbench.model import InputError, default_draft, normalize_draft
from workbench.service import export_project, validate_project
from workbench.store import Store
from test_workbench import draft
import test_registry_validation as registry_tests


class PortablePackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Store(Path(self.temp.name))

    def project(self, **changes):
        values = draft(kind="agent-skill", trigger="Use when defining a bounded scope.")
        values.update(changes)
        return self.store.create(normalize_draft(values)[0])

    def test_new_default_and_legacy_records(self):
        self.assertEqual(default_draft()["kind"], "agent-skill")
        legacy = self.project(kind="assistant", target="openai-custom-gpt")
        # Simulate a pre-change database record, with none of the new fields.
        with self.store._connect() as connection:
            row = connection.execute("SELECT draft_json FROM projects WHERE id=?", (legacy["id"],)).fetchone()
            value = json.loads(row[0])
            for key in ("trigger", "conversion_notes", "adapter_platform", "tool_requirements"):
                value.pop(key)
            connection.execute("UPDATE projects SET draft_json=? WHERE id=?", (json.dumps(value), legacy["id"]))
        existing = self.store.get(legacy["id"])
        self.assertEqual(existing["kind"], "assistant")
        self.assertEqual(existing["target"], "openai-custom-gpt")
        with zipfile.ZipFile(io.BytesIO(export_project(existing, self.store)[1])) as archive:
            self.assertIn("prompts/system.md", archive.namelist())
            self.assertNotIn("skills/scope-guide/SKILL.md", archive.namelist())

    def test_all_product_kinds_export_self_contained_skill_and_unverified_plan(self):
        for kind in ("agent-skill", "plugin", "connector"):
            with self.subTest(kind=kind):
                project = self.project(kind=kind, adapter_platform="Example host, format to verify",
                                       tool_requirements="Read-only MCP tool, owner authentication required.",
                                       conversion_notes="Retrieval behavior is unverified.")
                self.assertEqual([], validate_project(project)["errors"])
                with zipfile.ZipFile(io.BytesIO(export_project(project, self.store)[1])) as archive:
                    skill = archive.read("skills/scope-guide/SKILL.md").decode()
                    frontmatter = yaml.safe_load(skill.split("---", 2)[1])
                    self.assertEqual(frontmatter["name"], "scope-guide")
                    self.assertIn("when", frontmatter["description"])
                    self.assertIn("skills/scope-guide/LICENSE.md", archive.namelist())
                    self.assertIn("bounded recommendation", archive.read("skills/scope-guide/references/procedure.md").decode())
                    plan = json.loads(archive.read("adapters/plan.json"))
                    self.assertFalse(plan["installable"])
                    self.assertEqual(plan["compatibility"], [])
                    self.assertEqual(plan["product_kind"], kind)
                    manifest = yaml.safe_load(archive.read("manifest.yaml"))
                    self.assertEqual(manifest["deployment_surfaces"], [])
                    self.assertEqual(manifest["packaging"]["storage"], "private-external")
                    self.assertIn("Retrieval behavior is unverified.", archive.read("docs/conversion.md").decode())

    def test_invalid_skill_and_incomplete_adapter_are_blocked(self):
        for changes in ({"slug": "x" * 65}, {"trigger": ""}, {"trigger": "x" * 1025}, {"kind": "plugin"}, {"kind": "connector"}):
            with self.subTest(changes=changes):
                project = self.project(**changes)
                self.assertFalse(validate_project(project)["valid"])
                with self.assertRaises(InputError):
                    export_project(project, self.store)

    def test_new_fields_survive_save_and_protected_exports_remain_private(self):
        project = self.project(bfs_firewall=True, conversion_notes="Owner supplied mapping.")
        restored = Store(Path(self.temp.name)).get(project["id"])
        self.assertEqual(restored["conversion_notes"], "Owner supplied mapping.")
        with zipfile.ZipFile(io.BytesIO(export_project(restored, self.store)[1])) as archive:
            manifest = yaml.safe_load(archive.read("manifest.yaml"))
            self.assertEqual(manifest["visibility_control"]["visibility_lock"], "permanent-private")
            self.assertEqual(manifest["visibility_control"]["visibility"], "private")
            schema = yaml.safe_load((Path(__file__).resolve().parents[1] / "schemas/manifest.schema.yaml").read_text(encoding="utf-8"))
            manifest["packaging"]["storage"] = "public-subtree"
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.Draft202012Validator(schema).validate(manifest)

    def test_backup_round_trip_preserves_adapter_and_conversion_fields(self):
        project = self.project(kind="connector", adapter_platform="Example host",
                               tool_requirements="Read-only API; no credentials embedded.",
                               conversion_notes="Action maps to the host adapter.")
        with tempfile.TemporaryDirectory() as target:
            restored = Store(Path(target))
            restored.import_backup(self.store.backup())
            saved = restored.get(project["id"])
            for field in ("kind", "trigger", "adapter_platform", "tool_requirements", "conversion_notes"):
                self.assertEqual(project[field], saved[field])


class SubtreeMigrationTests(unittest.TestCase):
    def setUp(self):
        registry_tests.RegistryValidationTests.setUp(self)

    def check(self, data):
        return registry_tests.RegistryValidationTests.check(self, data)

    def test_private_or_protected_entry_cannot_enter_public_subtree(self):
        for index in (0, 4, 7):
            data = copy.deepcopy(self.data)
            data["repositories"][index]["migration"]["storage"] = "public-subtree"
            self.assertTrue(self.check(data))

    def test_migration_requires_safe_unique_path_and_source_commit(self):
        for field, value in (("destination", "capabilities/../secret"),
                             ("destination", self.data["repositories"][1]["migration"]["destination"]),
                             ("status", "imported"), ("source_commit", "invented")):
            data = copy.deepcopy(self.data)
            data["repositories"][0]["migration"][field] = value
            self.assertTrue(self.check(data))

    def test_approved_public_record_can_target_subtree(self):
        data = copy.deepcopy(self.data)
        entry = data["repositories"][0]
        entry["visibility"] = "public"
        entry["migration"].update(storage="public-subtree", status="source-inventoried", source_commit="a" * 40)
        self.assertEqual([], self.check(data))


if __name__ == "__main__":
    unittest.main()
