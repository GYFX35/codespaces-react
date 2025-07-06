import re
from urllib.parse import urlparse
from .heuristics import (
    URGENCY_KEYWORDS,
    SENSITIVE_INFO_KEYWORDS,
    TOO_GOOD_TO_BE_TRUE_KEYWORDS,
    GENERIC_GREETINGS,
    TECH_SUPPORT_SCAM_KEYWORDS,
    PAYMENT_KEYWORDS,
    URL_PATTERN,
    SUSPICIOUS_TLDS,
    CRYPTO_ADDRESS_PATTERNS,
    PHONE_NUMBER_PATTERN,
    HEURISTIC_WEIGHTS,
)

# Pre-compile a regex for suspicious TLDs for efficiency if used frequently
# This creates a pattern like: \.(xyz|top|loan|club|...)$
# Ensure TLDs are escaped if they contain special regex characters (none in current list)
SUSPICIOUS_TLD_REGEX = re.compile(
    r"\.(" + "|".join(tld.lstrip(".") for tld in SUSPICIOUS_TLDS) + r")$", re.IGNORECASE
)

# Keywords that might appear in URLs that are suspicious (especially if not on a primary domain)
SUSPICIOUS_URL_PATH_KEYWORDS = [
    "login",
    "verify",
    "account",
    "secure",
    "update",
    "signin",
    "banking",
    "password",
]


def analyze_text_for_scams(text_content):
    """
    Analyzes a block of text content for various scam indicators.

    Args:
        text_content (str): The text to analyze.

    Returns:
        dict: A dictionary containing:
              'score' (float): An overall scam likelihood score.
              'indicators_found' (list): A list of strings describing found indicators.
              'urls_analyzed' (list): A list of dicts for each URL found and its analysis.
    """
    if not text_content:
        return {"score": 0.0, "indicators_found": [], "urls_analyzed": []}

    text_lower = text_content.lower()  # For case-insensitive keyword matching
    score = 0.0
    indicators_found = []
    urls_analyzed_details = []

    # 1. Keyword-based checks
    keyword_checks = {
        "URGENCY": URGENCY_KEYWORDS,
        "SENSITIVE_INFO": SENSITIVE_INFO_KEYWORDS,
        "TOO_GOOD_TO_BE_TRUE": TOO_GOOD_TO_BE_TRUE_KEYWORDS,
        "GENERIC_GREETING": GENERIC_GREETINGS,
        "TECH_SUPPORT": TECH_SUPPORT_SCAM_KEYWORDS,
        "PAYMENT_REQUEST": PAYMENT_KEYWORDS,
    }

    for category, keywords in keyword_checks.items():
        for keyword in keywords:
            if keyword in text_lower:
                message = f"Presence of '{category.replace('_', ' ').title()}' keyword: '{keyword}'"
                indicators_found.append(message)
                score += HEURISTIC_WEIGHTS.get(category, 1.0)
                # Optimization: could break after first keyword in category if only counting category once
                # For now, sum weights for each keyword hit to emphasize multiple indicators.

    # 2. Regex-based checks
    # URLs
    found_urls = URL_PATTERN.findall(text_content)
    for url_str in found_urls:
        url_analysis = {"url": url_str, "is_suspicious": False, "reasons": []}

        parsed_url = None
        try:
            # Add scheme if missing for urlparse
            if not url_str.startswith(("http://", "https://", "ftp://")):
                temp_url_str_for_parse = "http://" + url_str
            else:
                temp_url_str_for_parse = url_str
            parsed_url = urlparse(temp_url_str_for_parse)
        except Exception as e:
            # print(f"Warning: Could not parse URL '{url_str}': {e}")
            url_analysis["reasons"].append(f"Could not parse URL string.")
            # Continue with regex checks on url_str itself if parsing fails

        # Check for suspicious TLDs
        domain_to_check = (
            parsed_url.hostname if parsed_url else url_str
        )  # Fallback to full string if parse failed
        if domain_to_check and SUSPICIOUS_TLD_REGEX.search(domain_to_check):
            reason = f"URL uses a potentially suspicious TLD (e.g., {SUSPICIOUS_TLD_REGEX.search(domain_to_check).group(0)})"
            url_analysis["reasons"].append(reason)
            url_analysis["is_suspicious"] = True
            score += HEURISTIC_WEIGHTS.get("SUSPICIOUS_TLD", 1.0)

        # Check for suspicious keywords in URL path/query or domain itself
        # (e.g. yourbank.com.suspicious.xyz/login or secure-payment-verify.com)
        # This is a simple check; more advanced would involve checking against known legit domains.
        for keyword in SUSPICIOUS_URL_PATH_KEYWORDS:
            if keyword in url_str.lower():  # Check the whole URL string
                # Avoid flagging legit sites like "myaccount.google.com" just for "account"
                # This needs refinement: only flag if domain is not a known major one.
                # For MVP, this check is broad.
                is_known_major_domain = False
                if parsed_url and parsed_url.hostname:
                    known_domains = [
                        "google.com",
                        "facebook.com",
                        "amazon.com",
                        "apple.com",
                        "microsoft.com",
                        "paypal.com",
                    ]  # Example list
                    for kd in known_domains:
                        if parsed_url.hostname.endswith(kd):
                            is_known_major_domain = True
                            break

                if not is_known_major_domain:
                    reason = f"URL contains suspicious keyword: '{keyword}'"
                    url_analysis["reasons"].append(reason)
                    url_analysis["is_suspicious"] = True
                    score += HEURISTIC_WEIGHTS.get("SUSPICIOUS_URL_KEYWORD", 1.0)
                    break  # Only count one such keyword per URL for now

        if url_analysis["is_suspicious"]:
            indicators_found.append(
                f"Suspicious URL found: {url_str} (Reasons: {'; '.join(url_analysis['reasons'])})"
            )
        urls_analyzed_details.append(url_analysis)

    # Crypto Addresses
    for crypto_name, pattern in CRYPTO_ADDRESS_PATTERNS.items():
        if pattern.search(
            text_content
        ):  # Search original text, not lowercased, as patterns might be case-sensitive
            message = f"Potential {crypto_name} cryptocurrency address found."
            indicators_found.append(message)
            score += HEURISTIC_WEIGHTS.get("CRYPTO_ADDRESS", 2.0)

    # Phone Numbers (Presence alone is not a strong indicator, context matters, which is hard for MVP)
    # For MVP, we'll just note if one is found. The weighting is important here.
    if PHONE_NUMBER_PATTERN.search(text_content):
        message = "Phone number detected in text."
        indicators_found.append(message)
        score += HEURISTIC_WEIGHTS.get("PHONE_NUMBER_UNSOLICITED", 0.25)  # Low weight

    # TODO: Add more heuristics like:
    # - Grammar/spelling (complex, likely requires external library for good results)
    # - Sense of urgency combined with financial request
    # - Analysis of sender (if email headers were available)

    return {
        "score": round(score, 2),
        "indicators_found": indicators_found,
        "urls_analyzed": urls_analyzed_details,
    }


if __name__ == "__main__":
    test_cases = [
        {
            "name": "Phishing Attempt",
            "text": "Dear Customer, your account is suspended due to unusual activity. Please verify your password at http://yourbank.secure-login-update.xyz/verify immediately. Act now to avoid closure.",
            "expected_min_score": 5.0,  # URGENCY, SENSITIVE_INFO, SUSPICIOUS_TLD, SUSPICIOUS_URL_KEYWORD
        },
        {
            "name": "Prize Scam",
            "text": "CONGRATULATIONS YOU WON!!! You've won a free iPhone! Claim your reward now at www.totally-real-prize.top/claim-123. Provide your details to receive your prize.",
            "expected_min_score": 4.0,  # TOO_GOOD_TO_BE_TRUE, SENSITIVE_INFO, SUSPICIOUS_TLD
        },
        {
            "name": "Tech Support Scam",
            "text": "Microsoft Support Alert: Your computer is infected with a virus! Call immediately 1-800-FAKE-TECH for a technician to get remote access. Your IP address compromised.",
            "expected_min_score": 4.0,  # TECH_SUPPORT, URGENCY, PHONE_NUMBER
        },
        {
            "name": "Crypto Payment Scam",
            "text": "Urgent payment needed for outstanding invoice. Send 0.5 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa to settle your account.",
            "expected_min_score": 4.0,  # URGENCY, PAYMENT_REQUEST, CRYPTO_ADDRESS
        },
        {
            "name": "Legitimate-sounding Message",
            "text": "Hello John, just a reminder about our meeting tomorrow at 10 AM. Please find the agenda attached. Website: www.ourcompany.com. Call me if you have questions: (123) 456-7890",
            "expected_max_score": 2.0,  # Might pick up phone number, or URL if not whitelisted
        },
        {
            "name": "Generic Greeting Email",
            "text": "Dear valued customer, We are updating our terms of service. No action needed from your side. Visit https://realcompany.com/terms for details.",
            "expected_max_score": 1.0,  # GENERIC_GREETING
        },
        {
            "name": "URL with suspicious keyword but known domain",
            "text": "Please login to your account at https://myaccount.google.com/login-activity to check recent activity.",
            "expected_max_score": 0.5,  # Should not flag "login" or "account" heavily due to known domain
        },
    ]

    for case in test_cases:
        print(f"\n--- Test Case: {case['name']} ---")
        print(
            f"Text: \"{case['text'][:100]}...\""
            if len(case["text"]) > 100
            else f"Text: \"{case['text']}\""
        )
        results = analyze_text_for_scams(case["text"])
        print(f"Score: {results['score']}")
        print("Indicators:")
        for indicator in results["indicators_found"]:
            print(f"  - {indicator}")
        if results["urls_analyzed"]:
            print("URLs Analyzed:")
            for url_info in results["urls_analyzed"]:
                print(
                    f"  - URL: {url_info['url']}, Suspicious: {url_info['is_suspicious']}, Reasons: {url_info.get('reasons', [])}"
                )

        if "expected_min_score" in case:
            assert (
                results["score"] >= case["expected_min_score"]
            ), f"Score {results['score']} was less than expected min {case['expected_min_score']}"
            print(f"Assertion: Score >= {case['expected_min_score']} PASSED")
        if "expected_max_score" in case:
            assert (
                results["score"] <= case["expected_max_score"]
            ), f"Score {results['score']} was more than expected max {case['expected_max_score']}"
            print(f"Assertion: Score <= {case['expected_max_score']} PASSED")

    print("\n--- Test with empty text ---")
    empty_results = analyze_text_for_scams("")
    assert empty_results["score"] == 0.0
    assert not empty_results["indicators_found"]
    print("Empty text test passed.")

    print("\nCore analysis engine tests completed.")
