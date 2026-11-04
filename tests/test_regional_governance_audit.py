"""Evidence, protection, and immutability checks for the regional audit."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "regional_governance_audit",
    ROOT / "scripts" / "regional-governance-audit.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RegionalGovernanceAuditTests(unittest.TestCase):
    @staticmethod
    def mentor_binding() -> dict[str, str]:
        return {
            key: MODULE.MENTOR_REVIEW[key]
            for key in ("repository", "revision", "path")
        }

    def copy_fixture(self, tmp: str) -> Path:
        root = Path(tmp)
        (root / "registry").mkdir()
        (root / "schemas").mkdir()
        (root / "scripts").mkdir()
        (root / "registry/index.yaml").write_text(
            (ROOT / "registry/index.yaml").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (root / "schemas/registry.schema.yaml").write_text(
            (ROOT / "schemas/registry.schema.yaml").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (root / "scripts/check-registry.py").write_text(
            (ROOT / "scripts/check-registry.py").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        return root

    def test_clean_report_passes_controls_but_defers_adoption(self):
        report = MODULE.build_report(ROOT)
        self.assertEqual(report["audit"]["status"], "PASS")
        self.assertEqual(report["audit"]["adoption"], "DEFERRED")
        self.assertEqual(report["owner_approval"]["status"], "PENDING")
        self.assertTrue(report["registry"]["unchanged_during_audit"])
        self.assertEqual(report["protected_client_records"]["violations"], [])
        tiers = {item["claim"]: item["tier"] for item in report["evidence"]}
        self.assertEqual(
            tiers["The named OverKill mentor surface has the stated governance or graduation behavior."],
            "CONFIRMED",
        )
        self.assertEqual(
            report["mentor_review"]["revision"],
            "8de1eb212d8db193fd22eb85bf0843f366a0c1a7",
        )
        self.assertEqual(
            report["mentor_review"]["path"],
            "scripts/public-graduation-audit.py",
        )
        self.assertEqual(report["mentor_review"]["reviewer"], "Replit Agent")

    def test_baseline_digest_is_required_to_match(self):
        digest = hashlib.sha256(
            (ROOT / "registry/index.yaml").read_bytes()
        ).hexdigest()
        self.assertEqual(
            MODULE.build_report(ROOT, baseline_sha256=digest)["audit"]["status"],
            "PASS",
        )
        self.assertEqual(
            MODULE.build_report(ROOT, baseline_sha256="0" * 64)["audit"]["status"],
            "FAIL",
        )

    def test_protected_record_sweep_catches_visibility_downgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy_fixture(tmp)
            registry_path = root / "registry/index.yaml"
            data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            data["repositories"][8]["visibility"] = "public"
            registry_path.write_text(yaml.safe_dump(data), encoding="utf-8")
            report = MODULE.build_report(root)
            self.assertEqual(report["audit"]["status"], "FAIL")
            self.assertTrue(report["protected_client_records"]["violations"])

    def test_approval_must_match_scope_and_registry_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy_fixture(tmp)
            registry_digest = hashlib.sha256(
                (root / "registry/index.yaml").read_bytes()
            ).hexdigest()
            approval = {
                "audit": MODULE.AUDIT_NAME,
                "scope": MODULE.AUDIT_SCOPE,
                "adaptation": MODULE.ADAPTATION_ID,
                "decision": "approve",
                "owner": "OKHP3",
                "approved_at": "2026-09-14",
                "registry_sha256": registry_digest,
                "mentor_review": self.mentor_binding(),
                "publication_decision": "not-authorized",
                "hosting_decision": "not-authorized",
                "boundary_review": {
                    "reviewed_at": "2026-09-14",
                    "registry_sha256": registry_digest,
                    "controls": {
                        control: "CONFIRMED"
                        for control in MODULE.REQUIRED_BOUNDARY_CONTROLS
                    },
                    "residual_limits": ["Downloaded export custody remains external."],
                },
            }
            approval_path = root / "approval.yaml"
            approval_path.write_text(yaml.safe_dump(approval), encoding="utf-8")
            report = MODULE.build_report(root, approval_path=approval_path)
            self.assertEqual(report["owner_approval"]["status"], "APPROVED")
            self.assertEqual(
                report["owner_approval"]["mentor_review"],
                self.mentor_binding(),
            )
            adaptation_claim = next(
                item for item in report["evidence"]
                if item["claim"].startswith("The approved narrow adaptation")
            )
            self.assertEqual(adaptation_claim["tier"], "INFERRED")
            self.assertNotIn(
                "Owner has not recorded a valid decision for this exact adaptation, scope, registry digest, pinned mentor source, and release boundaries.",
                report["remaining_unknowns"],
            )
            self.assertEqual(report["audit"]["adoption"], "DEFERRED")

            changed = copy.deepcopy(approval)
            changed["scope"] = "public-graduation"
            approval_path.write_text(yaml.safe_dump(changed), encoding="utf-8")
            report = MODULE.build_report(root, approval_path=approval_path)
            self.assertEqual(report["owner_approval"]["status"], "INVALID")
            self.assertEqual(
                next(
                    item for item in report["evidence"]
                    if item["claim"].startswith("The approved narrow adaptation")
                )["tier"],
                "PROPOSAL",
            )
            self.assertIn(
                "Owner has not recorded a valid decision for this exact adaptation, scope, registry digest, pinned mentor source, and release boundaries.",
                report["remaining_unknowns"],
            )

            changed = copy.deepcopy(approval)
            changed["boundary_review"]["registry_sha256"] = "0" * 64
            approval_path.write_text(yaml.safe_dump(changed), encoding="utf-8")
            report = MODULE.build_report(root, approval_path=approval_path)
            self.assertEqual(report["owner_approval"]["status"], "INVALID")
            self.assertIn(
                "boundary_review.registry_sha256 does not match the current registry",
                report["owner_approval"]["reason"],
            )

    def test_approval_is_invalidated_when_pinned_mentor_revision_or_path_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy_fixture(tmp)
            registry_digest = hashlib.sha256(
                (root / "registry/index.yaml").read_bytes()
            ).hexdigest()
            approval_path = root / "approval.yaml"
            decision = {
                "audit": MODULE.AUDIT_NAME,
                "scope": MODULE.AUDIT_SCOPE,
                "adaptation": MODULE.ADAPTATION_ID,
                "decision": "approve",
                "owner": "OKHP3",
                "decided_at": "2026-11-04",
                "registry_sha256": registry_digest,
                "mentor_review": self.mentor_binding(),
                "publication_decision": "not-authorized",
                "hosting_decision": "not-authorized",
                "boundary_review": {
                    "reviewed_at": "2026-11-04",
                    "registry_sha256": registry_digest,
                    "controls": {
                        control: "CONFIRMED"
                        for control in MODULE.REQUIRED_BOUNDARY_CONTROLS
                    },
                    "residual_limits": ["Downloaded export custody remains external."],
                },
            }
            approval_path.write_text(yaml.safe_dump(decision), encoding="utf-8")

            original_mentor_review = dict(MODULE.MENTOR_REVIEW)
            try:
                for field, new_value in (
                    ("revision", "a" * 40),
                    ("path", "scripts/another-audit.py"),
                ):
                    with self.subTest(field=field):
                        MODULE.MENTOR_REVIEW[field] = new_value
                        report = MODULE.build_report(root, approval_path=approval_path)
                        self.assertEqual(report["owner_approval"]["status"], "INVALID")
                        self.assertIn(
                            f"mentor_review.{field} does not match the pinned mentor review",
                            report["owner_approval"]["reason"],
                        )
                        MODULE.MENTOR_REVIEW[field] = original_mentor_review[field]
            finally:
                MODULE.MENTOR_REVIEW.clear()
                MODULE.MENTOR_REVIEW.update(original_mentor_review)

    def test_cli_requires_current_pinned_mentor_revision_and_path(self):
        registry_digest = hashlib.sha256(
            (ROOT / "registry/index.yaml").read_bytes()
        ).hexdigest()
        approval = {
            "audit": MODULE.AUDIT_NAME,
            "scope": MODULE.AUDIT_SCOPE,
            "adaptation": MODULE.ADAPTATION_ID,
            "decision": "approve",
            "owner": "OKHP3",
            "decided_at": "2026-11-04",
            "registry_sha256": registry_digest,
            "mentor_review": self.mentor_binding(),
            "publication_decision": "not-authorized",
            "hosting_decision": "not-authorized",
            "boundary_review": {
                "reviewed_at": "2026-11-04",
                "registry_sha256": registry_digest,
                "controls": {
                    control: "CONFIRMED"
                    for control in MODULE.REQUIRED_BOUNDARY_CONTROLS
                },
                "residual_limits": ["Downloaded export custody remains external."],
            },
        }
        script = ROOT / "scripts" / "regional-governance-audit.py"

        with tempfile.TemporaryDirectory() as tmp:
            approval_path = Path(tmp) / "approval.yaml"
            for field, stale_value in (
                ("revision", "a" * 40),
                ("path", "scripts/another-audit.py"),
            ):
                with self.subTest(field=field):
                    stale_approval = copy.deepcopy(approval)
                    stale_approval["mentor_review"][field] = stale_value
                    approval_path.write_text(
                        yaml.safe_dump(stale_approval), encoding="utf-8"
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(script),
                            "--require-approval",
                            "--owner-approval",
                            str(approval_path),
                        ],
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    report = json.loads(result.stdout)

                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(report["owner_approval"]["status"], "INVALID")
                    self.assertIn(
                        f"mentor_review.{field} does not match the pinned mentor review",
                        report["owner_approval"]["reason"],
                    )

            approval_path.write_text(yaml.safe_dump(approval), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--require-approval",
                    "--owner-approval",
                    str(approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            report = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(report["owner_approval"]["status"], "APPROVED")

    def test_approval_requires_each_boundary_control_to_be_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy_fixture(tmp)
            registry_digest = hashlib.sha256(
                (root / "registry/index.yaml").read_bytes()
            ).hexdigest()
            approval_path = root / "approval.yaml"
            approval_path.write_text(
                yaml.safe_dump(
                    {
                        "audit": MODULE.AUDIT_NAME,
                        "scope": MODULE.AUDIT_SCOPE,
                        "adaptation": MODULE.ADAPTATION_ID,
                        "decision": "approve",
                        "owner": "OKHP3",
                        "decided_at": "2026-11-04",
                        "registry_sha256": registry_digest,
                        "mentor_review": self.mentor_binding(),
                        "publication_decision": "not-authorized",
                        "hosting_decision": "not-authorized",
                        "boundary_review": {
                            "reviewed_at": "2026-11-04",
                            "registry_sha256": registry_digest,
                            "controls": {
                                control: "CONFIRMED"
                                for control in MODULE.REQUIRED_BOUNDARY_CONTROLS
                            },
                            "residual_limits": ["Downloaded export custody remains external."],
                        },
                    }
                ),
                encoding="utf-8",
            )
            decision = yaml.safe_load(approval_path.read_text(encoding="utf-8"))
            decision["boundary_review"]["controls"]["private_exports"] = "UNKNOWN"
            approval_path.write_text(yaml.safe_dump(decision), encoding="utf-8")

            report = MODULE.build_report(root, approval_path=approval_path)

        self.assertEqual(report["owner_approval"]["status"], "INVALID")
        self.assertIn(
            "boundary_review.controls.private_exports must be CONFIRMED",
            report["owner_approval"]["reason"],
        )

    def test_defer_decision_is_recorded_without_authorizing_adoption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy_fixture(tmp)
            registry_digest = hashlib.sha256(
                (root / "registry/index.yaml").read_bytes()
            ).hexdigest()
            decision_path = root / "decision.yaml"
            decision_path.write_text(
                yaml.safe_dump(
                    {
                        "audit": MODULE.AUDIT_NAME,
                        "scope": MODULE.AUDIT_SCOPE,
                        "adaptation": MODULE.ADAPTATION_ID,
                        "decision": "defer",
                        "owner": "OKHP3",
                        "decided_at": "2026-09-17",
                        "registry_sha256": registry_digest,
                        "mentor_review": self.mentor_binding(),
                        "publication_decision": "not-authorized",
                        "hosting_decision": "not-authorized",
                    }
                ),
                encoding="utf-8",
            )

            report = MODULE.build_report(root, approval_path=decision_path)

            self.assertEqual(report["owner_approval"]["status"], "DEFERRED")
            self.assertEqual(report["owner_approval"]["decision"], "defer")
            self.assertEqual(report["audit"]["adoption"], "DEFERRED")
            self.assertNotIn(
                "Owner has not recorded a valid decision for this exact adaptation, scope, registry digest, pinned mentor source, and release boundaries.",
                report["remaining_unknowns"],
            )

    def test_decision_cannot_be_reused_for_a_different_release_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy_fixture(tmp)
            registry_digest = hashlib.sha256(
                (root / "registry/index.yaml").read_bytes()
            ).hexdigest()
            decision = {
                "audit": MODULE.AUDIT_NAME,
                "scope": MODULE.AUDIT_SCOPE,
                "adaptation": MODULE.ADAPTATION_ID,
                "decision": "defer",
                "owner": "OKHP3",
                "decided_at": "2026-09-17",
                "registry_sha256": registry_digest,
                "mentor_review": self.mentor_binding(),
                "publication_decision": "not-authorized",
                "hosting_decision": "not-authorized",
            }
            decision_path = root / "decision.yaml"
            for field, value in (
                ("publication_decision", "manual-pages-release"),
                ("hosting_decision", "hosted-authoring"),
            ):
                with self.subTest(field=field):
                    changed = dict(decision)
                    changed[field] = value
                    decision_path.write_text(
                        yaml.safe_dump(changed), encoding="utf-8"
                    )
                    report = MODULE.build_report(
                        root, approval_path=decision_path
                    )
                    self.assertEqual(
                        report["owner_approval"]["status"], "INVALID"
                    )

    def test_non_mapping_approval_preserves_an_invalid_evidence_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy_fixture(tmp)
            approval_path = root / "approval.yaml"
            for content in ("", "null", "approved", "42", "[]", "- approve"):
                with self.subTest(content=content):
                    approval_path.write_text(content, encoding="utf-8")
                    report = MODULE.build_report(root, approval_path=approval_path)
                    self.assertEqual(report["owner_approval"]["status"], "INVALID")
                    self.assertEqual(report["audit"]["adoption"], "DEFERRED")
                    self.assertTrue(report["registry"]["unchanged_during_audit"])


if __name__ == "__main__":
    unittest.main()
