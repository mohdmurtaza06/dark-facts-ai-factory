import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from factory.quality_gate import validate_video


GOOD = {
    "format": {"duration": "60.0", "size": "500000"},
    "streams": [
        {"codec_type": "video", "width": 1080, "height": 1920, "codec_name": "h264"},
        {"codec_type": "audio", "codec_name": "aac"},
    ],
}


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.video = Path(self.tmp.name) / "sample.mp4"
        self.video.write_bytes(b"x" * 150_000)

    def tearDown(self):
        self.tmp.cleanup()

    @patch("factory.quality_gate.probe_video", return_value=GOOD)
    def test_accepts_valid_vertical_short(self, _probe):
        self.assertEqual(validate_video(self.video), [])

    @patch("factory.quality_gate.probe_video", return_value={
        "format": {"duration": "30"},
        "streams": [{"codec_type": "video", "width": 720, "height": 1280, "codec_name": "vp9"}],
    })
    def test_rejects_wrong_duration_resolution_codec_and_missing_audio(self, _probe):
        errors = validate_video(self.video)
        self.assertTrue(any("Duration" in e for e in errors))
        self.assertTrue(any("1080x1920" in e for e in errors))
        self.assertTrue(any("H.264" in e for e in errors))
        self.assertTrue(any("Missing audio" in e for e in errors))

    def test_rejects_missing_file(self):
        self.assertTrue(validate_video(self.video.parent / "missing.mp4"))


if __name__ == "__main__":
    unittest.main()
