from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yaml"
PUBLIC_ARTIFACT_BUILDER = ROOT / "scripts" / "build-public-artifact.py"
TEST_ACTOR = "pages-release-test-actor"


def load_public_artifact_builder():
    spec = importlib.util.spec_from_file_location(
        "pages_release_public_artifact_builder",
        PUBLIC_ARTIFACT_BUILDER,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the public artifact builder")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    return builder


class PagesReleaseWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        cls.steps = cls.workflow["jobs"]["build"]["steps"]

    def test_release_is_manual_and_permissions_stay_narrow(self) -> None:
        triggers = self.workflow.get("on", self.workflow.get(True))
        self.assertIsInstance(triggers, dict)
        self.assertEqual(set(triggers), {"workflow_dispatch"})

        self.assertEqual(
            self.workflow["permissions"],
            {
                "contents": "read",
                "pages": "write",
                "id-token": "write",
            },
        )
        for job_name, job in self.workflow["jobs"].items():
            with self.subTest(job=job_name):
                self.assertNotIn("permissions", job)

    def step_named(self, name: str) -> dict:
        return next(step for step in self.steps if step.get("name") == name)

    def test_initiator_is_recorded_before_build_failures_and_survives_failure(self) -> None:
        names = [step.get("name") for step in self.steps]
        record_index = names.index("Record manual release initiator")
        checkout_index = names.index("Checkout repository")
        artifact_index = names.index("Build public artifact")
        self.assertLess(record_index, checkout_index)
        self.assertLess(record_index, artifact_index)

        record_step = self.steps[record_index]
        self.assertEqual(
            record_step["env"]["RELEASE_ACTOR"],
            "${{ github.actor }}",
        )
        self.assertNotIn("RELEASE_ACTOR", self.workflow.get("env", {}))

        with tempfile.TemporaryDirectory() as directory:
            summary = Path(directory) / "step-summary.md"
            env = os.environ.copy()
            env.update(
                {
                    "RELEASE_ACTOR": TEST_ACTOR,
                    "GITHUB_STEP_SUMMARY": str(summary),
                }
            )
            record_result = subprocess.run(
                ["bash", "-e", "-c", record_step["run"]],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(record_result.returncode, 0, record_result.stderr)
            failure_result = subprocess.run(
                ["bash", "-e", "-c", "exit 23"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(failure_result.returncode, 23)
            summary_text = summary.read_text(encoding="utf-8")

        self.assertIn(
            f"- Started by: `{TEST_ACTOR}`",
            summary_text,
        )

    def test_initiator_is_not_copied_into_public_pages_artifact(self) -> None:
        builder = load_public_artifact_builder()
        artifact_step = self.step_named("Build public artifact")
        self.assertNotIn("RELEASE_ACTOR", artifact_step.get("env", {}))

        with tempfile.TemporaryDirectory(prefix="pages-release-test-", dir=ROOT) as directory:
            builder.OUTPUT = Path(directory) / "pages"
            builder.build()

            artifact_files = [
                path for path in builder.OUTPUT.rglob("*") if path.is_file()
            ]
            self.assertTrue(artifact_files, "public artifact should contain files")
            for path in artifact_files:
                with self.subTest(path=path.relative_to(builder.OUTPUT)):
                    self.assertNotIn(
                        TEST_ACTOR.encode("utf-8"),
                        path.read_bytes(),
                    )

    def test_public_checksum_manifest_is_uploaded_separately_with_retention(self) -> None:
        names = [step.get("name") for step in self.steps]
        manifest_index = names.index("Write public file checksum manifest")
        upload_index = names.index("Upload Pages checksum manifest")
        pages_index = names.index("Upload Pages artifact")
        self.assertLess(names.index("Build public artifact"), manifest_index)
        self.assertLess(manifest_index, upload_index)
        self.assertLess(upload_index, pages_index)

        manifest_step = self.steps[manifest_index]
        self.assertEqual(
            manifest_step["run"],
            'python scripts/build-public-artifact.py --release-file-manifest > "$RUNNER_TEMP/pages-checksum-manifest.json"',
        )

        upload_step = self.steps[upload_index]
        self.assertEqual(upload_step["uses"], "actions/upload-artifact@v7")
        self.assertEqual(
            upload_step["with"],
            {
                "name": "askjamie-pages-checksum-manifest",
                "path": "${{ runner.temp }}/pages-checksum-manifest.json",
                "if-no-files-found": "error",
                "retention-days": 30,
            },
        )

    def test_deploy_job_uses_release_manifest_for_live_file_verification(self) -> None:
        deploy_steps = self.workflow["jobs"]["deploy"]["steps"]
        names = [step.get("name") for step in deploy_steps]
        download = next(
            step for step in deploy_steps
            if step.get("name") == "Download Pages checksum manifest"
        )
        verify = next(
            step for step in deploy_steps
            if step.get("name") == "Verify deployed page content"
        )

        self.assertEqual(download["uses"], "actions/download-artifact@v8")
        self.assertEqual(
            download["with"],
            {
                "name": "askjamie-pages-checksum-manifest",
                "path": "${{ runner.temp }}/pages-release",
                "digest-mismatch": "error",
            },
        )
        self.assertLess(names.index(download["name"]), names.index("Deploy to GitHub Pages"))
        self.assertLess(names.index("Deploy to GitHub Pages"), names.index(verify["name"]))
        self.assertIn("--verify-release-manifest", verify["run"])
        self.assertIn(
            "$RUNNER_TEMP/pages-release/pages-checksum-manifest.json",
            verify["run"],
        )


if __name__ == "__main__":
    unittest.main()
