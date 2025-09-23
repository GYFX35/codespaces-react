import re
import urllib.request
import requests
import os
from urllib.parse import urlparse
from textblob import TextBlob
from .heuristics import (
    URGENCY_KEYWORDS,
    SENSITIVE_INFO_KEYWORDS,
    TOO_GOOD_TO_BE_TRUE_KEYWORDS,
    GENERIC_GREETINGS,
    TECH_SUPPORT_SCAM_KEYWORDS,
    PAYMENT_KEYWORDS,
    URL_PATTERN,
    SUSPICIOUS_TLDS,
    FINANCIAL_ADDRESS_PATTERNS,
    PHONE_NUMBER_PATTERN,
    HEURISTIC_WEIGHTS,
    LEGITIMATE_DOMAINS,
    SUSPICIOUS_URL_PATTERNS
)

def check_google_safe_browsing(url, api_key):
    """
    Checks a URL against the Google Safe Browsing API.
    Returns a tuple: (is_suspicious, reason)
    """
    if not api_key:
        return False, "Google Safe Browsing API key not configured."

    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {
            "clientId": "social-media-analyzer",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "matches" in data:
                threat_type = data["matches"][0]["threatType"]
                return True, f"Flagged by Google Safe Browsing as {threat_type}."
            else:
                return False, "Clean according to Google Safe Browsing."
        else:
            return False, f"Google Safe Browsing API error: {response.status_code}"
    except requests.RequestException as e:
        return False, f"Could not connect to Google Safe Browsing: {e}"

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

def is_url_suspicious(url, platform=None, api_key=None):
    """
    Checks if a URL is suspicious based on various patterns and lists,
    including Google Safe Browsing.
    Returns a tuple: (bool_is_suspicious, reason_string)
    """
    # 1. Google Safe Browsing Check
    if api_key:
        is_susp, reason = check_google_safe_browsing(url, api_key)
        if is_susp:
            return True, reason

    # 2. Local Heuristics
    normalized_url = url.lower()
    domain = get_domain_from_url(url)
    legitimate_domains = get_legitimate_domains(platform)

    # Check if the domain is in the legitimate list for the platform
    if domain in legitimate_domains:
        # Still check for impersonation patterns that might include the legit domain
        for pattern in SUSPICIOUS_URL_PATTERNS:
            if re.search(pattern, normalized_url, re.IGNORECASE):
                if not domain.endswith(tuple(legitimate_domains)):
                    return True, f"URL impersonates a legitimate domain: {pattern}"
        return False, "URL domain is on the legitimate list."

    # Check against known suspicious patterns
    for pattern in SUSPICIOUS_URL_PATTERNS:
        if re.search(pattern, normalized_url, re.IGNORECASE):
            return True, f"URL matches suspicious pattern: {pattern}"

    # Check for suspicious TLDs
    suspicious_tld_regex = re.compile(r"\.(" + "|".join(tld.lstrip('.') for tld in SUSPICIOUS_TLDS) + r")$", re.IGNORECASE)
    if suspicious_tld_regex.search(domain):
        return True, f"URL uses a potentially suspicious TLD."

    # Check if a known legitimate service name is part of the domain, but it's not official
    for service in LEGITIMATE_DOMAINS.keys():
        if service != "general" and service in domain:
            return True, f"URL contains the name of a legitimate service ('{service}') but is not an official domain."

    return False, "URL does not match common suspicious patterns."

def analyze_text_for_scams(text_content, platform=None, api_key=None):
    """
    Analyzes a block of text content for various scam indicators.
    """
    if not text_content:
        return {"score": 0.0, "indicators_found": [], "urls_analyzed": []}

    text_lower = text_content.lower()
    score = 0.0
    indicators_found = []
    urls_analyzed_details = []

    # 1. Sentiment Analysis
    blob = TextBlob(text_content)
    if blob.sentiment.polarity < -0.5:
        message = "Strong negative sentiment detected in text."
        if message not in indicators_found:
            indicators_found.append(message)
            score += HEURISTIC_WEIGHTS.get("NEGATIVE_SENTIMENT", 2.0)

    # 2. Keyword-based checks
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

    # 3. Regex-based checks
    found_urls = URL_PATTERN.findall(text_content)
    for url_str in found_urls:
        is_susp, reason = is_url_suspicious(url_str, platform, api_key)
        url_analysis = {"url": url_str, "is_suspicious": is_susp, "reason": reason}
        if is_susp:
            # Increase score significantly if flagged by Google
            if "Google Safe Browsing" in reason:
                score += HEURISTIC_WEIGHTS.get("GOOGLE_SAFE_BROWSING_HIT", 10.0)
            else:
                score += HEURISTIC_WEIGHTS.get("SUSPICIOUS_URL_PATTERN", 3.0)
            indicators_found.append(f"Suspicious URL found: {url_str} (Reason: {reason})")
        urls_analyzed_details.append(url_analysis)

    # 4. Financial Identifiers
    for id_name, pattern in FINANCIAL_ADDRESS_PATTERNS.items():
        if pattern.search(text_content):
            message = f"Potential {id_name} identifier found."
            if message not in indicators_found:
                indicators_found.append(message)
                score += HEURISTIC_WEIGHTS.get(f"{id_name}_ADDRESS", 2.5)

    # 5. Phone Numbers
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

def analyze_url_content(url):
    """
    Fetches the content of a URL and analyzes it for scams.
    """
    try:
        # Add a user-agent to avoid being blocked by some websites
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                html_content = response.read().decode('utf-8', errors='ignore')
                # Simple regex to strip HTML tags, not perfect but avoids new dependencies
                text_content = re.sub(r'<[^>]+>', '', html_content)
                return analyze_text_for_scams(text_content, platform="general_web")
            else:
                return {"error": f"Failed to fetch URL: HTTP status code {response.status}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
