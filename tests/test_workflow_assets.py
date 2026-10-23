"""Проверяет публичный набор укрупнённых workflow-команд."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMMANDS = ROOT / ".cursor" / "commands"
SKILLS = ROOT / ".cursor" / "skills"
PUBLIC_COMMANDS = {
    "do-ask-questions",
    "do-plan-and-specs",
    "do-tdd-loop",
    "do-review",
    "do-branch-to-master",
}


class WorkflowAssetsTests(unittest.TestCase):
    def test_public_commands_have_matching_skills(self):
        for name in PUBLIC_COMMANDS:
            with self.subTest(name=name):
                self.assertTrue((COMMANDS / f"{name}.md").is_file())
                skill = SKILLS / name / "SKILL.md"
                self.assertTrue(skill.is_file())
                text = skill.read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", text)
                self.assertIn("## Чеклист", text)

    def test_branch_to_master_keeps_required_promotion_steps(self):
        text = (SKILLS / "do-branch-to-master" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "Push источника MR",
            "MR в `master` + approve + merge",
            "git -C $prod fetch origin --prune",
            "git -C $prod checkout master",
            "git -C $prod pull --ff-only origin master",
            "Залито на прод <название ветки>:",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
