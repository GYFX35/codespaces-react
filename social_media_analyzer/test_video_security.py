import unittest
from .video_security_analyzer import analyze_video_metadata

class TestVideoSecurity(unittest.TestCase):
    def test_video_metadata_ai(self):
        metadata = "This is a deepfake video of a celebrity using face swap technology. It has unnatural blinking."
        result = analyze_video_metadata(metadata)
        self.assertGreater(result["score"], 4.0)
        self.assertIn("Found AI video keyword: 'deepfake'", result["indicators_found"])

    def test_video_metadata_safe(self):
        metadata = "A beautiful sunset over the mountains, filmed with a drone."
        result = analyze_video_metadata(metadata)
        self.assertEqual(result["score"], 0)

if __name__ == '__main__':
    unittest.main()
