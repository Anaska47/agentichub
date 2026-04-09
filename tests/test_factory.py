import unittest
from pathlib import Path
import shutil

from factory.core import build_candidates, load_strategy, pick_batch, write_batch
from factory.doctor import collect_environment_status
from factory.mobile import androidize_source, build_package_id


class FactoryTests(unittest.TestCase):
    def test_build_candidates_produces_unique_slugs(self):
        strategy = load_strategy(None)
        candidates = build_candidates(strategy)
        slugs = [item.slug for item in candidates]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_pick_batch_spreads_mechanics(self):
        strategy = load_strategy(None)
        candidates = build_candidates(strategy)
        batch = pick_batch(candidates, count=3, seed=7)
        mechanics = {item.mechanic for item in batch}
        self.assertGreaterEqual(len(mechanics), 2)

    def test_write_batch_creates_figma_and_github_artifacts(self):
        strategy = load_strategy(None)
        candidates = build_candidates(strategy)
        batch = pick_batch(candidates, count=2, seed=7)

        tmpdir = Path("tests/.tmp-output")
        if tmpdir.exists():
            shutil.rmtree(tmpdir)

        try:
            root = write_batch(tmpdir, batch)
            self.assertTrue((root / "portfolio" / "github-repo-plan.md").exists())
            self.assertTrue((root / "portfolio" / "figma-batch-handoff.md").exists())

            first_app = Path(root / batch[0].slug)
            self.assertTrue((first_app / "docs" / "figma-handoff.md").exists())
            self.assertTrue((first_app / "docs" / "github-backlog.md").exists())
            self.assertTrue((first_app / "docs" / "code-connect-targets.json").exists())
            self.assertTrue((first_app / ".github" / "pull_request_template.md").exists())
        finally:
            if tmpdir.exists():
                shutil.rmtree(tmpdir)

    def test_androidize_source_creates_capacitor_and_fastlane_files(self):
        strategy = load_strategy(None)
        candidates = build_candidates(strategy)
        batch = pick_batch(candidates, count=1, seed=7)

        batch_dir = Path("tests/.tmp-batch")
        export_dir = Path("tests/.tmp-android")
        for path in (batch_dir, export_dir):
            if path.exists():
                shutil.rmtree(path)

        try:
            write_batch(batch_dir, batch)
            androidize_source(batch_dir, export_dir, package_prefix="com.anaska.agentichub")

            app_root = export_dir / batch[0].slug
            expected_package = build_package_id("com.anaska.agentichub", batch[0].slug)

            self.assertTrue((export_dir / "android-batch.json").exists())
            self.assertTrue((app_root / "package.json").exists())
            self.assertTrue((app_root / "capacitor.config.json").exists())
            self.assertTrue((app_root / "docs" / "android-release.md").exists())
            self.assertTrue((app_root / "docs" / "admob-integration.md").exists())
            self.assertTrue((app_root / "fastlane" / "metadata" / "android" / "en-US" / "title.txt").exists())
            self.assertIn(expected_package, (app_root / "capacitor.config.json").read_text(encoding="utf-8"))
        finally:
            for path in (batch_dir, export_dir):
                if path.exists():
                    shutil.rmtree(path)

    def test_doctor_reports_expected_tools(self):
        statuses = collect_environment_status()
        names = {item.name for item in statuses}
        self.assertTrue({"python", "node", "npm", "git", "java", "android-sdk", "adb"}.issubset(names))


if __name__ == "__main__":
    unittest.main()
