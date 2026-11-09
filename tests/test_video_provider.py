import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from factory.video_provider import (
    VideoProviderConfigurationError,
    VideoProviderError,
    generate_scene_clip,
)


class VideoProviderTests(unittest.TestCase):
    def test_requires_explicit_model_and_token(self):
        with self.assertRaises(VideoProviderConfigurationError):
            generate_scene_clip("A cinematic scene", "out.mp4", model=None, token=None)

    def test_saves_valid_mp4_bytes(self):
        payload = b"\x00\x00\x00\x18ftypisom" + (b"x" * 1200)
        client = Mock()
        client.text_to_video.return_value = payload
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "scene.mp4"
            result = generate_scene_clip(
                "A cinematic scene", target, client=client,
                model="test/model", token="test-token"
            )
            self.assertEqual(result, target)
            self.assertEqual(target.read_bytes(), payload)
            client.text_to_video.assert_called_once()

    def test_rejects_non_mp4_response(self):
        client = Mock()
        client.text_to_video.return_value = b"<html>" + (b"x" * 1200)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(VideoProviderError):
                generate_scene_clip(
                    "A cinematic scene", Path(tmp) / "scene.mp4",
                    client=client, model="test/model", token="test-token"
                )

    def test_rejects_empty_prompt(self):
        with self.assertRaises(ValueError):
            generate_scene_clip("  ", "out.mp4", model="test/model", token="test-token")


if __name__ == "__main__":
    unittest.main()
