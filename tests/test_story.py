import unittest
from factory.story import build_storyboard
from factory.content import load_json, FACTS

class StoryTests(unittest.TestCase):
    def test_octopus_six_scenes(self):
        facts = load_json(FACTS, [])
        fact = next(f for f in facts if f["id"] == "octopus-hearts")
        sb = build_storyboard(fact)
        self.assertEqual(len(sb["scenes"]), 6)
        self.assertAlmostEqual(sb["total_duration"], 20.0, delta=0.5)
        self.assertEqual(sb["character"]["name"], "Octo")
        self.assertTrue(sb["script"])
        for sc in sb["scenes"]:
            self.assertIn("narration", sc)
            self.assertIn("camera", sc)
            self.assertGreater(sc["duration"], 0)

if __name__ == "__main__":
    unittest.main()
