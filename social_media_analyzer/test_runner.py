from social_media_analyzer.scam_detector import analyze_text_for_scams

if __name__ == '__main__':
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
