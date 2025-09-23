import unittest
from .scam_detector import analyze_text_for_scams

class TestScamDetector(unittest.TestCase):

    def test_sentiment_analysis(self):
        # Test case for negative sentiment
        text_negative = "This is a terrible, awful, no good, very bad message."
        result_negative = analyze_text_for_scams(text_negative)
        self.assertIn("Strong negative sentiment detected in text.", [indicator for indicator in result_negative["indicators_found"]])

        # Test case for positive sentiment
        text_positive = "This is a wonderful, amazing, great message."
        result_positive = analyze_text_for_scams(text_positive)
        self.assertNotIn("Strong negative sentiment detected in text.", [indicator for indicator in result_positive["indicators_found"]])

    def test_keyword_matching(self):
        # Test case for urgency keyword
        text_urgency = "URGENT: Your account has been compromised."
        result_urgency = analyze_text_for_scams(text_urgency)
        self.assertIn("Presence of 'Urgency' keyword: 'urgent'", [indicator for indicator in result_urgency["indicators_found"]])

        # Test case for stemming
        text_stemming = "I need you to verify your account immediately."
        result_stemming = analyze_text_for_scams(text_stemming)
        self.assertIn("Presence of 'Sensitive Info' keyword: 'verify your account'", [indicator for indicator in result_stemming["indicators_found"]])

if __name__ == '__main__':
    unittest.main()
