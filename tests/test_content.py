import json
import tempfile
import unittest
from pathlib import Path
from factory import content

class ContentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.old_facts, self.old_used = content.FACTS, content.USED
        self.addCleanup(self.restore_paths)
        self.facts_path = root / "facts.json"
        self.used_path = root / "used_facts.json"
        self.facts_path.write_text(json.dumps([
            {"id": "a", "topic": "Space", "hook": "Space is strange!", "fact": "A reviewed fact.", "short_fact": "Short fact.", "source": "https://example.org/a"},
            {"id": "b", "topic": "Ocean", "hook": "The ocean is strange!", "fact": "Another reviewed fact.", "short_fact": "Another short fact.", "source": "https://example.org/b"},
            {"id": "c", "topic": "Animals", "hook": "Animals are strange!", "fact": "A third reviewed fact.", "short_fact": "Third short fact.", "source": "https://example.org/c"}
        ]), encoding="utf-8")
        content.FACTS, content.USED = self.facts_path, self.used_path

    def restore_paths(self):
        content.FACTS, content.USED = self.old_facts, self.old_used

    def test_selects_unique_facts(self):
        chosen = content.choose_facts(2)
        self.assertEqual(len(chosen), 2)
        self.assertEqual(len({f["id"] for f in chosen}), 2)

    def test_fact_rotation_uses_remaining_then_resets(self):
        first = content.choose_facts(2)
        second = content.choose_facts(1)
        self.assertNotEqual(first[0]["id"], second[0]["id"])
        third = content.choose_facts(2)
        self.assertEqual(len(third), 2)

    def test_metadata_has_provenance_and_short_title(self):
        package = content.build_package({
            "id": "x", "topic": "Space", "hook": "A surprising fact!",
            "fact": "A factual sentence.", "short_fact": "A short summary.",
            "source": "https://example.org"
        })
        self.assertIn("https://example.org", package["description"])
        self.assertLessEqual(len(package["title"]), 100)
        self.assertIn("A factual sentence.", package["script"])
        self.assertIn("\n\nSource:", package["description"])

if __name__ == "__main__":
    unittest.main()
