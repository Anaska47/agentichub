import unittest
from pathlib import Path
import shutil

from factory.core import build_candidates, load_strategy, pick_batch, write_batch


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


if __name__ == "__main__":
    unittest.main()
