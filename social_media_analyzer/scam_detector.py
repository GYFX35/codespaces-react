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
    LEGITIMATE_DOMAINS,
    SUSPICIOUS_URL_PATTERNS
)

def get_legitimate_domains(platform=None):
    """
    Returns a list of legitimate domains for a given platform,
    including general safe domains.
    """
    domains = set(LEGITIMATE_DOMAINS.get("general", []))
    if platform and platform in LEGITIMATE_DOMAINS:
        domains.update(LEGITIMATE_DOMAINS[platform])
    return list(domains)

def get_domain_from_url(url):
    """Extracts the domain (e.g., 'example.com') from a URL."""
    if "://" in url:
        domain = url.split("://")[1].split("/")[0].split("?")[0]
    else:
        domain = url.split("/")[0].split("?")[0]
    return domain.lower()

def is_url_suspicious(url, platform=None):
    """
    Checks if a URL is suspicious based on various patterns and lists.
    Returns a tuple: (bool_is_suspicious, reason_string)
    """
    normalized_url = url.lower()
    domain = get_domain_from_url(url)
    legitimate_domains = get_legitimate_domains(platform)

    # 1. Check if the domain is in the legitimate list for the platform
    if domain in legitimate_domains:
        # Still check for impersonation patterns that might include the legit domain
        for pattern in SUSPICIOUS_URL_PATTERNS:
            if re.search(pattern, normalized_url, re.IGNORECASE):
                if not domain.endswith(tuple(legitimate_domains)):
                    return True, f"URL impersonates a legitimate domain: {pattern}"
        return False, "URL domain is on the legitimate list."

    # 2. Check against known suspicious patterns
    for pattern in SUSPICIOUS_URL_PATTERNS:
        if re.search(pattern, normalized_url, re.IGNORECASE):
            return True, f"URL matches suspicious pattern: {pattern}"

    # 3. Check for suspicious TLDs
    suspicious_tld_regex = re.compile(r"\.(" + "|".join(tld.lstrip('.') for tld in SUSPICIOUS_TLDS) + r")$", re.IGNORECASE)
    if suspicious_tld_regex.search(domain):
        return True, f"URL uses a potentially suspicious TLD."

    # 4. Check if a known legitimate service name is part of the domain, but it's not official
    for service in LEGITIMATE_DOMAINS.keys():
        if service != "general" and service in domain:
            return True, f"URL contains the name of a legitimate service ('{service}') but is not an official domain."

    return False, "URL does not match common suspicious patterns."

def analyze_text_for_scams(text_content, platform=None):
    """
    Analyzes a block of text content for various scam indicators.
    """
    if not text_content:
        return {"score": 0.0, "indicators_found": [], "urls_analyzed": []}

    text_lower = text_content.lower()
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
                if message not in indicators_found:
                    indicators_found.append(message)
                    score += HEURISTIC_WEIGHTS.get(category, 1.0)

    # 2. Regex-based checks
    found_urls = URL_PATTERN.findall(text_content)
    for url_str in found_urls:
        is_susp, reason = is_url_suspicious(url_str, platform)
        url_analysis = {"url": url_str, "is_suspicious": is_susp, "reason": reason}
        if is_susp:
            score += HEURISTIC_WEIGHTS.get("SUSPICIOUS_URL_PATTERN", 3.0)
            indicators_found.append(f"Suspicious URL found: {url_str} (Reason: {reason})")
        urls_analyzed_details.append(url_analysis)

    # 3. Crypto Addresses
    for crypto_name, pattern in CRYPTO_ADDRESS_PATTERNS.items():
        if pattern.search(text_content):
            message = f"Potential {crypto_name} cryptocurrency address found."
            if message not in indicators_found:
                indicators_found.append(message)
                score += HEURISTIC_WEIGHTS.get("CRYPTO_ADDRESS", 2.5)

    # 4. Phone Numbers
    if PHONE_NUMBER_PATTERN.search(text_content):
        message = "Phone number detected in text."
        if message not in indicators_found:
            indicators_found.append(message)
            score += HEURISTIC_WEIGHTS.get("PHONE_NUMBER_UNSOLICITED", 1.0)

    return {
        "score": round(score, 2),
        "indicators_found": indicators_found,
        "urls_analyzed": urls_analyzed_details
    }

if __name__ == '__main__':
    # Example Usage
    test_message = "URGENT: Your Instagram account has unusual activity. Please verify your account now by clicking http://instagram.security-update.com/login to avoid suspension."
    analysis_result = analyze_text_for_scams(test_message, platform="instagram")
    print(f"--- Analyzing Instagram Scam Message ---")
    print(f"Message: {test_message}")
    print(f"Score: {analysis_result['score']}")
    print("Indicators:")
    for indicator in analysis_result['indicators_found']:
        print(f"  - {indicator}")

    test_message_whatsapp = "Hey, check out this link: http://wa.me/1234567890. Also, please send money to my bitcoin wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    analysis_result_whatsapp = analyze_text_for_scams(test_message_whatsapp, platform="whatsapp")
    print(f"\n--- Analyzing WhatsApp Message ---")
    print(f"Message: {test_message_whatsapp}")
    print(f"Score: {analysis_result_whatsapp['score']}")
    print("Indicators:")
    for indicator in analysis_result_whatsapp['indicators_found']:
        print(f"  - {indicator}")
