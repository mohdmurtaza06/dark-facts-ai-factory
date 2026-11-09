import unittest
from factory.story import build_storyboard
from factory.content import load_json, FACTS

class StoryTests(unittest.TestCase):
    def test_all_facts_have_distinct_topic_aware_storyboards(self):
        facts = load_json(FACTS, [])
        self.assertGreaterEqual(len(facts), 5)
        storyboards = [build_storyboard(f) for f in facts]
        self.assertEqual(len({s["fact_id"] for s in storyboards}), len(storyboards))
        for sb in storyboards:
            self.assertEqual(len(sb["scenes"]), 6)
            self.assertAlmostEqual(sb["total_duration"], 20.0, delta=0.1)
            self.assertTrue(sb["script"])
            self.assertEqual(sb["topic"], next(f["topic"] for f in facts if f["id"] == sb["fact_id"]))
            self.assertIn("visual_profile", sb)
            self.assertIn("subject", sb["visual_profile"])
            for scene in sb["scenes"]:
                self.assertIn("narration", scene)
                self.assertIn("camera", scene)
                self.assertIn("visual_profile", scene)
                self.assertGreater(scene["duration"], 0)

    def test_space_and_animal_topics_use_different_visual_profiles(self):
        facts = load_json(FACTS, [])
        by_id = {f["id"]: f for f in facts}
        space = build_storyboard(by_id["venus-day"])
        animal = build_storyboard(by_id["wombat-poop"])
        self.assertNotEqual(space["visual_profile"]["subject"], animal["visual_profile"]["subject"])
        self.assertNotEqual(space["visual_profile"]["theme"], animal["visual_profile"]["theme"])

if __name__ == "__main__":
    unittest.main()
