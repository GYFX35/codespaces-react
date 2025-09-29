import unittest
from .teen_protection import (
    analyze_for_cyberbullying,
    analyze_for_inappropriate_content,
    analyze_for_privacy_risks
)

class TestTeenProtection(unittest.TestCase):

    def test_cyberbullying(self):
        """Test the cyberbullying detection."""
        # Test case with bullying keywords
        text1 = "You are such a loser and an idiot."
        result1 = analyze_for_cyberbullying(text1)
        self.assertGreater(result1['score'], 0)
        self.assertIn("Detected potential cyberbullying keyword: 'loser'", result1['indicators_found'])
        self.assertIn("Detected potential cyberbullying keyword: 'idiot'", result1['indicators_found'])

        # Test case with no bullying keywords
        text2 = "Have a great day!"
        result2 = analyze_for_cyberbullying(text2)
        self.assertEqual(result2['score'], 0)
        self.assertEqual(len(result2['indicators_found']), 0)

    def test_inappropriate_content(self):
        """Test the inappropriate content detection."""
        # Test case with inappropriate keywords
        text1 = "Don't send nudes or talk about drugs."
        result1 = analyze_for_inappropriate_content(text1)
        self.assertGreater(result1['score'], 0)
        self.assertIn("Detected potential inappropriate content keyword: 'send nudes'", result1['indicators_found'])
        self.assertIn("Detected potential inappropriate content keyword: 'drugs'", result1['indicators_found'])

        # Test case with no inappropriate keywords
        text2 = "This is a perfectly normal conversation."
        result2 = analyze_for_inappropriate_content(text2)
        self.assertEqual(result2['score'], 0)
        self.assertEqual(len(result2['indicators_found']), 0)

    def test_privacy_risks(self):
        """Test the privacy risk detection."""
        # Test case with privacy risk keywords
        text1 = "My address is 123 Main St and my phone number is 555-1234."
        result1 = analyze_for_privacy_risks(text1)
        self.assertGreater(result1['score'], 0)
        self.assertIn("Detected potential privacy risk keyword: 'my address is'", result1['indicators_found'])
        self.assertIn("Detected potential privacy risk keyword: 'my phone number is'", result1['indicators_found'])

        # Test case with no privacy risk keywords
        text2 = "I like to talk about my hobbies."
        result2 = analyze_for_privacy_risks(text2)
        self.assertEqual(result2['score'], 0)
        self.assertEqual(len(result2['indicators_found']), 0)

    def test_empty_input(self):
        """Test empty input for all analysis types."""
        result_cb = analyze_for_cyberbullying("")
        self.assertEqual(result_cb['score'], 0)
        self.assertEqual(len(result_cb['indicators_found']), 0)

        result_ic = analyze_for_inappropriate_content("")
        self.assertEqual(result_ic['score'], 0)
        self.assertEqual(len(result_ic['indicators_found']), 0)

        result_pr = analyze_for_privacy_risks("")
        self.assertEqual(result_pr['score'], 0)
        self.assertEqual(len(result_pr['indicators_found']), 0)

if __name__ == '__main__':
    unittest.main()