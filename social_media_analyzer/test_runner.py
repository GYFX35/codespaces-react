import unittest
from unittest.mock import patch, Mock
from .scam_detector import analyze_text_for_scams
from .test_teen_protection import TestTeenProtection

def run_manual_tests():
    # Example Usage
    test_cases = {
        "Instagram Phishing": {
            "message": "URGENT: Your Instagram account has unusual activity. Please verify your account now by clicking http://instagram.security-update.com/login to avoid suspension.",
            "platform": "instagram"
        },
        "WhatsApp Crypto Scam": {
            "message": "Hey, check out this link: http://wa.me/1234567890. Also, please send money to my bitcoin wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "platform": "whatsapp"
        },
        "PayPal Phishing": {
            "message": "Your PayPal account has been limited. Please log in to http://paypal-support-uk.com/login to restore access. Your invoice is attached.",
            "platform": "paypal"
        },
        "Stripe Phishing": {
            "message": "There was a problem with your recent payment on Stripe. Please update your payment information at http://stripe-billing-update.com",
            "platform": "stripe"
        },
        "Payoneer Scam": {
            "message": "Congratulations! You've received a payment of $5000 via Payoneer. Please confirm your details at http://payoneer.rewards.xyz to claim your funds.",
            "platform": "payoneer"
        },
        "Bank Transfer Fraud": {
            "message": "Urgent invoice payment required. Please transfer the amount to IBAN DE89370400440532013000, SWIFT/BIC COBADEFFXXX. Your account will be suspended otherwise.",
            "platform": "banks"
        },
        "Kuaishou Benign Case": {
            "message": "Check out my new video on www.kwai.com/my-awesome-video! #kuaishou",
            "platform": "kuaishou"
        },
        "Kuaishou Phishing Attempt": {
            "message": "URGENT: Your Kuaishou account is at risk! Verify at http://kuaishou-login.net to secure it and get free followers.",
            "platform": "kuaishou"
        }
    }

    for name, data in test_cases.items():
        analysis_result = analyze_text_for_scams(data["message"], platform=data["platform"])
        print(f"\n--- Analyzing: {name} ---")
        print(f"Message: {data['message']}")
        print(f"Score: {analysis_result['score']}")
        print("Indicators:")
        for indicator in analysis_result['indicators_found']:
            print(f"  - {indicator}")
        print("URLs Analyzed:")
        for url_info in analysis_result['urls_analyzed']:
            print(f"  - URL: {url_info['url']}, Suspicious: {url_info['is_suspicious']}, Reason: {url_info['reason']}")

class TestScamDetector(unittest.TestCase):
    @patch('social_media_analyzer.scam_detector.requests.post')
    def test_google_safe_browsing_malicious(self, mock_post):
        # Mock the API response for a malicious URL
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "matches": [
                {
                    "threatType": "MALWARE",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": "http://malware.testing.google.test/testing/malware/"},
                }
            ]
        }
        mock_post.return_value = mock_response

        message = "check this out http://malware.testing.google.test/testing/malware/"
        result = analyze_text_for_scams(message, api_key="fake_key")

        self.assertTrue(any("Google Safe Browsing" in reason for reason in result["indicators_found"]))
        self.assertEqual(result['urls_analyzed'][0]['is_suspicious'], True)

    @patch('social_media_analyzer.scam_detector.requests.post')
    def test_google_safe_browsing_clean(self, mock_post):
        # Mock the API response for a clean URL
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        message = "this is a clean site http://www.google.com"
        result = analyze_text_for_scams(message, api_key="fake_key")

        self.assertFalse(any("Google Safe Browsing" in reason for reason in result["indicators_found"]))
        self.assertEqual(result['urls_analyzed'][0]['is_suspicious'], False)

if __name__ == '__main__':
    run_manual_tests()
    # Run unit tests
    scam_suite = unittest.makeSuite(TestScamDetector)
    teen_suite = unittest.makeSuite(TestTeenProtection)
    all_tests = unittest.TestSuite([scam_suite, teen_suite])

    runner = unittest.TextTestRunner()
    print("\n--- Running All Unit Tests ---")
    result = runner.run(all_tests)
    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print("Some tests failed.")
