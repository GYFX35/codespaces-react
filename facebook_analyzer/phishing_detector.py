import re

# Keywords common in phishing messages
PHISHING_KEYWORDS = [
    "verify your account", "update your details", "confirm your identity",
    "login required", "secure your account", "account suspended",
    "unusual activity", "security alert", "important notification",
    "action required", "limited time offer", "winner", "prize",
    "confidential", "urgent", "immediate attention", "access restricted",
    "card declined", "payment issue", "invoice", "refund"
]

# Patterns for suspicious URLs
# Order matters: more specific/dangerous patterns should come first.
SUSPICIOUS_URL_PATTERNS = [
    # Attempts to impersonate legitimate domains by using them as subdomains of a malicious domain
    # e.g., facebook.com.malicious.com, login-facebook.com-site.org
    r"https?://(?:[a-z0-9\-]+\.)*(?:facebook|fb|instagram|whatsapp)\.com\.[a-z0-9\-]+\.[a-z]+",
    r"https?://(?:[a-z0-9\-]+\.)*facebook-[a-z0-9\-]+\.[a-z]+",
    r"https?://(?:[a-z0-9\-]+\.)*fb-[a-z0-9\-]+\.[a-z]+",
    # Common URL shorteners (can be legitimate but often used in phishing)
    r"https?://bit\.ly",
    r"https?://goo\.gl",
    r"https?://t\.co", # Twitter shortener, often abused
    # IP Address URLs
    r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    # Generic keywords in domain that are often suspicious if not part of a known legit service
    # e.g., "login", "secure", "account", "update" in a non-standard TLD or unfamiliar domain
    r"https?://[^/]*(?:login|secure|account|update|verify|support|admin)[^/]*\.(?:biz|info|tk|ml|ga|cf|gq|xyz|club|top|loan|work|online|site)",
    # Very long subdomains or many hyphens (common obfuscation)
    r"https?://(?:[a-z0-9\-]+\.){4,}", # 4 or more subdomains
    r"https?://[^/]*\-.*\-.*\-.*[a-z]+", # multiple hyphens in domain part
]

LEGITIMATE_DOMAINS = [
    "facebook.com",
    "www.facebook.com",
    "m.facebook.com",
    "fb.com", # Official Facebook shortener
    "www.fb.com",
    "instagram.com",
    "www.instagram.com",
    "whatsapp.com",
    "www.whatsapp.com",
    "google.com", # For test cases
    "www.google.com",
    "amazon.com", # For test cases
    "www.amazon.com"
]

def extract_urls(text):
    """Extracts URLs from a given text."""
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.findall(url_pattern, text)

def get_domain_from_url(url):
    """Extracts the domain (e.g., 'example.com') from a URL."""
    if "://" in url:
        domain = url.split("://")[1].split("/")[0].split("?")[0]
    else: # Handles www.example.com cases without http(s)
        domain = url.split("/")[0].split("?")[0]
    return domain.lower()

def is_url_suspicious(url):
    """
    Checks if a URL is suspicious.
    Returns a tuple: (bool_is_suspicious, reason_string)
    """
    normalized_url_for_pattern_matching = url.lower()
    domain = get_domain_from_url(url)

    # 1. Check against explicit legitimate domains
    # This is a strong signal that it *might* be okay, but phishing can still occur on legit sites (e.g., compromised page).
    # However, for this tool, if the *domain itself* is legit, we'll primarily rely on other indicators for now.
    if domain in LEGITIMATE_DOMAINS:
        # We could add checks here for suspicious paths on legitimate domains,
        # but that's more complex. For now, if the core domain is legit,
        # we won't flag it based on domain alone.
        # Let's still check if it matches any *very specific* impersonation patterns
        # that might accidentally include a legit domain name within them.
        for pattern in [
            r"https?://(?:[a-z0-9\-]+\.)*(?:facebook|fb|instagram|whatsapp)\.com\.[a-z0-9\-]+\.[a-z]+", #e.g. facebook.com.hacker.com
            r"https?://(?:[a-z0-9\-]+\.)*facebook-[a-z0-9\-]+\.[a-z]+" #e.g. my-facebook-login.hacker.com
        ]:
            if re.search(pattern, normalized_url_for_pattern_matching, re.IGNORECASE):
                 # Check if the *actual domain* is the legit one, not just contained.
                 # e.g. "facebook.com.hacker.com" contains "facebook.com" but domain is "hacker.com"
                if not domain.endswith("facebook.com"): # Simplified check for this example
                    return True, f"URL impersonates a legitimate domain: {pattern}"
        return False, "URL domain is on the legitimate list."

    # 2. Check against known suspicious patterns (these should be more specific)
    for pattern in SUSPICIOUS_URL_PATTERNS:
        if re.search(pattern, normalized_url_for_pattern_matching, re.IGNORECASE):
            return True, f"URL matches suspicious pattern: {pattern}"

    # 3. Heuristic: Check if a known legitimate domain name is *part* of the domain,
    # but the domain itself is NOT on the legitimate list.
    # E.g., "facebook-login.some-other-site.com"
    for legit_substring in ["facebook", "fb", "instagram", "whatsapp"]:
        if legit_substring in domain:
            # We already checked if `domain` is in `LEGITIMATE_DOMAINS`.
            # So if we're here, it means `legit_substring` is in `domain`, but `domain` itself is not legit.
            return True, f"URL contains name of a legitimate service ('{legit_substring}') but is not an official domain."

    return False, "URL does not match common suspicious patterns and is not on the explicit legitimate list."


def analyze_message_for_phishing(message_text):
    """
    Analyzes a message for phishing indicators.
    Returns a dictionary with findings.
    """
    findings = {
        "score": 0, # Overall phishing likelihood score (higher is more suspicious)
        "keywords_found": [],
        "suspicious_urls_found": [],
        "urls_extracted": [],
        "summary": ""
    }

    # 1. Analyze text for keywords
    message_lower = message_text.lower()
    for keyword in PHISHING_KEYWORDS:
        if keyword in message_lower:
            findings["keywords_found"].append(keyword)
            findings["score"] += 1

    # 2. Extract and analyze URLs
    urls = extract_urls(message_text)
    findings["urls_extracted"] = urls
    for url in urls:
        is_susp, reason = is_url_suspicious(url)
        if is_susp:
            findings["suspicious_urls_found"].append({"url": url, "reason": reason})
            findings["score"] += 2 # Higher weight for suspicious URLs

    # 3. Generate summary
    if not findings["keywords_found"] and not findings["suspicious_urls_found"]:
        findings["summary"] = "No immediate phishing indicators found. However, always exercise caution with links and requests for information."
    else:
        summary_parts = []
        if findings["keywords_found"]:
            summary_parts.append(f"Found {len(findings['keywords_found'])} suspicious keyword(s): {', '.join(findings['keywords_found'])}.")
        if findings["suspicious_urls_found"]:
            summary_parts.append(f"Found {len(findings['suspicious_urls_found'])} suspicious URL(s).")
            for sus_url in findings["suspicious_urls_found"]:
                 summary_parts.append(f"  - {sus_url['url']} (Reason: {sus_url['reason']})")

        findings["summary"] = " ".join(summary_parts)
        if findings["score"] > 0:
             findings["summary"] += f" Overall phishing score: {findings['score']} (higher is more suspicious)."


    return findings

if __name__ == '__main__':
    # Example Usage
    original_test_messages = [
        ("URGENT: Your Facebook account has unusual activity. Please verify your account now by clicking http://facebook.security-update.com/login to avoid suspension.", "Original 1"),
        ("Hey, check out this cool site: www.google.com", "Original 2"),
        ("Your package is waiting for delivery. Update your shipping details here: http://bit.ly/fakepackage", "Original 3"),
        ("Hi, this is your bank. We need you to confirm your identity due to a login required. Please visit https://mybank.secure-access-point.net/confirm", "Original 4"),
        ("A login to your account from a new device was detected. If this wasn't you, please secure your account at http://123.45.67.89/facebook_login", "Original 5"),
        ("Click here to claim your prize! http://winner.com/prize-claim-form-xyz", "Original 6"),
        ("Official communication from Facebook: Please review our new terms at https://facebook.com/terms. This is important for your account security.", "Original 7")
    ]

    additional_test_messages = [
        ("Security Alert! Update your info at http://facebook.com.hacker.com and also check this http://bit.ly/anotherlink", "Additional 1: Multiple suspicious URLs"),
        ("URGENT: verify your account at https://facebook.com/security/alerts - this is a real link, but also check http://mysecurity-fb-check.com", "Additional 2: Mix of legit FB URL and suspicious one with keywords"),
        ("Hello there, how are you doing today?", "Additional 3: No keywords, no URLs"),
        ("Important security update from Facebook. Please login at https://www.facebook.com to review your settings. Your account safety is our priority.", "Additional 4: Keywords but legit URL"),
        ("Check this out: http://bit.ly/legitGoogleDoc - this could be a legit shortened link (hard to tell without unshortening)", "Additional 5: URL shortener, potentially legit content")
    ]

    all_test_messages = original_test_messages + additional_test_messages

    for i, (msg, label) in enumerate(all_test_messages):
        print(f"--- Analyzing Message ({label}) ---")
        print(f"Message: {msg}")
        analysis_result = analyze_message_for_phishing(msg)
        print(f"Score: {analysis_result['score']}")
        print(f"Keywords: {analysis_result['keywords_found']}")
        print(f"Suspicious URLs: {analysis_result['suspicious_urls_found']}")
        print(f"All URLs: {analysis_result['urls_extracted']}")
        print(f"Summary: {analysis_result['summary']}")
        print("-" * 30 + "\n")

    # Test URL suspicion logic directly
    print("\n--- Testing URL Suspicion Logic ---")
    test_urls = [
        "http://facebook.com.malicious.com/login.html",
        "https://www.facebook.com/officialpage",
        "http://fb.com-security-alert.com",
        "https://legit-service.com/facebook_integration", # Might be ok
        "http://192.168.1.10/phish",
        "https.google.com",
        "www.amazon.com/deals",
        "http://bit.ly/randomstuff",
        "https://totally-not-facebook.com",
        "http://facebook.com" # Should not be suspicious by default
    ]
    for url in test_urls:
        is_susp, reason = is_url_suspicious(url)
        print(f"URL: {url} -> Suspicious: {is_susp}, Reason: {reason}")
