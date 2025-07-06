import re

# --- Keyword Lists (case-insensitive matching will be applied) ---

# Keywords/phrases indicating urgency or pressure
URGENCY_KEYWORDS = [
    "urgent",
    "immediate action required",
    "act now",
    "limited time",
    "account suspended",
    "account will be closed",
    "final warning",
    "security alert",
    "unusual activity detected",
    "important notification",
    "don't delay",
    "expires soon",
    "offer ends today",
    "last chance",
    "your subscription will be cancelled",
    "payment declined",  # Removed "action needed"
]

# Keywords/phrases related to requests for sensitive information
SENSITIVE_INFO_KEYWORDS = [
    "verify your password",
    "confirm your password",
    "update your password",
    "password",
    "username",
    "login details",
    "credentials",
    "social security number",
    "ssn",
    "bank account",
    "account number",
    "routing number",
    "credit card number",
    "cvv",
    "pin number",
    "mother's maiden name",
    "security question",
    "confirm your details",
    "update your information",
    "verify your account",
    "provide your details",
    "personal information",
]

# Keywords/phrases indicating too-good-to-be-true offers, prizes, etc.
TOO_GOOD_TO_BE_TRUE_KEYWORDS = [
    "you have won",
    "you've won",
    "congratulations you won",
    "winner",
    "prize",
    "free gift",
    "claim your reward",
    "lottery",
    "sweepstakes",
    "guaranteed",
    "risk-free",
    "earn money fast",
    "work from home easy",
    "investment opportunity",
    "high return",
    "get rich quick",
    "inheritance",
    " unclaimed funds",
    "nigerian prince",  # Classic ones
]

# Generic greetings/salutations that can be suspicious in unsolicited contexts
GENERIC_GREETINGS = [
    "dear customer",
    "dear user",
    "dear valued customer",
    "dear account holder",
    "dear friend",
    "hello sir/madam",
    "greetings",
    # Note: "Hello" or "Hi" by themselves are too common to be reliably suspicious
]

# Keywords often found in tech support scams
TECH_SUPPORT_SCAM_KEYWORDS = [
    "microsoft support",
    "windows support",
    "apple support",
    "virus detected",
    "malware found",
    "your computer is infected",
    "call immediately",
    "technician",
    "remote access",
    "ip address compromised",
]

# Keywords related to payment requests or financial transactions
PAYMENT_KEYWORDS = [
    "payment",
    "invoice",
    "bill",
    "outstanding balance",
    "transfer funds",
    "wire transfer",
    "gift card",
    "cryptocurrency",
    "bitcoin",
    "western union",
    "moneygram",
    "urgent payment needed",
    "settle your account",
]


# --- Regular Expression Patterns ---

# Basic URL detection - this is simple and can be expanded
# It aims to find things that look like URLs. More sophisticated parsing will be needed
# if we want to break them down further or check TLDs more accurately here.
URL_PATTERN = re.compile(
    r"(?:(?:https?|ftp):\/\/|www\.)"  # http://, https://, ftp://, www.
    r"(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*"  # Non-space chars in URL
    r"(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])",  # Last char
    re.IGNORECASE,
)

# Suspicious Top-Level Domains (TLDs) - This list is not exhaustive!
# Scammers often use newer, cheaper, or less common TLDs.
SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".loan",
    ".club",
    ".work",
    ".online",
    ".biz",
    ".info",
    ".icu",
    ".gq",
    ".cf",
    ".tk",
    ".ml",  # Often free TLDs abused
    ".link",
    ".click",
    ".site",
    ".live",
    ".buzz",
    ".stream",
    ".download",
    # Sometimes, very long TLDs can be suspicious if combined with other factors
]
# Regex to check if a URL ends with one of these TLDs
# (Needs to be used after extracting the domain from a URL)
# Example: r"\.(xyz|top|loan)$" - will be built dynamically in analyzer

# Pattern for detecting strings that look like cryptocurrency addresses
CRYPTO_ADDRESS_PATTERNS = {
    "BTC": re.compile(
        r"\b(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{25,90})\b"
    ),
    "ETH": re.compile(r"\b(0x[a-fA-F0-9]{40})\b"),
    # Add more for other common cryptos like LTC, XMR if needed
}

# Pattern for phone numbers (very generic, adjust for specific country needs if possible)
# This is a basic example and might catch non-phone numbers or miss some valid ones.
# It aims for sequences of 7-15 digits, possibly with spaces, hyphens, or parentheses.
PHONE_NUMBER_PATTERN = re.compile(
    r"(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?(\d{3,4}[-.\s]?\d{3,4})"  # Simplified
    # r'(?:(?:\+|00)[1-9]\d{0,2}[-.\s]?)?(?:(?:\(\d{1,4}\)|\d{1,4})[-.\s]?)?(?:\d{1,4}[-.\s]?){1,4}\d{1,4}'
)


# --- Scoring Weights (Example - can be tuned) ---
# These weights can be used by the analyzer to calculate a scam score.
HEURISTIC_WEIGHTS = {
    "URGENCY": 1.5,
    "SENSITIVE_INFO": 2.5,
    "TOO_GOOD_TO_BE_TRUE": 2.0,
    "GENERIC_GREETING": 0.5,  # Lower weight as it's a weaker indicator alone
    "TECH_SUPPORT": 2.0,
    "PAYMENT_REQUEST": 1.5,
    "SUSPICIOUS_URL_KEYWORD": 1.0,  # e.g., "login," "verify" in URL path with non-primary domain
    "SUSPICIOUS_TLD": 2.0,
    "CRYPTO_ADDRESS": 2.5,  # Requesting crypto is often a scam indicator
    "PHONE_NUMBER_UNSOLICITED": 1.0,  # Presence of phone number in unsolicited mail could be for callback scam
    # "GRAMMAR_SPELLING": 0.5 (If implemented)
}


if __name__ == "__main__":
    print("--- Heuristic Definitions ---")
    print(f"Loaded {len(URGENCY_KEYWORDS)} urgency keywords.")
    print(f"Loaded {len(SENSITIVE_INFO_KEYWORDS)} sensitive info keywords.")
    print(f"Loaded {len(TOO_GOOD_TO_BE_TRUE_KEYWORDS)} too-good-to-be-true keywords.")
    print(f"Loaded {len(GENERIC_GREETINGS)} generic greetings.")
    print(f"Loaded {len(TECH_SUPPORT_SCAM_KEYWORDS)} tech support scam keywords.")
    print(f"Loaded {len(PAYMENT_KEYWORDS)} payment keywords.")

    print(f"\nURL Pattern: {URL_PATTERN.pattern}")
    print(f"Suspicious TLDs example: {SUSPICIOUS_TLDS[:5]}")

    print("\nCrypto Address Patterns:")
    for crypto, pattern in CRYPTO_ADDRESS_PATTERNS.items():
        print(f"  {crypto}: {pattern.pattern}")

    print(f"\nPhone Number Pattern: {PHONE_NUMBER_PATTERN.pattern}")

    print("\nHeuristic Weights:")
    for category, weight in HEURISTIC_WEIGHTS.items():
        print(f"  {category}: {weight}")

    # Test URL pattern
    test_text_with_urls = "Visit www.example.com or http://another-site.co.uk/path?query=1 and also https://test.xyz/secure"
    found_urls = URL_PATTERN.findall(test_text_with_urls)
    print(f"\nURLs found in test text: {found_urls}")
    assert len(found_urls) == 3

    # Test Crypto patterns
    btc_text = "Send 1 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa now!"
    eth_text = "My address is 0x1234567890abcdef1234567890abcdef12345678"
    no_crypto_text = "This is a normal message."

    assert CRYPTO_ADDRESS_PATTERNS["BTC"].search(btc_text)
    assert CRYPTO_ADDRESS_PATTERNS["ETH"].search(eth_text)
    assert not CRYPTO_ADDRESS_PATTERNS["BTC"].search(no_crypto_text)
    print("Crypto address pattern tests passed.")

    # Test phone number pattern (basic)
    phone_text_1 = "Call us at (123) 456-7890 for help."
    phone_text_2 = "Our number is +44 20 7946 0958."
    phone_text_3 = "Contact 1234567890."
    no_phone_text = "No number here."

    assert PHONE_NUMBER_PATTERN.search(phone_text_1)
    assert PHONE_NUMBER_PATTERN.search(phone_text_2)
    assert PHONE_NUMBER_PATTERN.search(phone_text_3)
    assert not PHONE_NUMBER_PATTERN.search(no_phone_text)
    print("Phone number pattern tests passed (basic).")

    print("\nHeuristics module loaded and basic regex patterns tested.")
