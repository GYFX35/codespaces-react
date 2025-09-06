import re

# --- Legitimate Domains ---
# This list helps the analyzer to recognize official domains and avoid flagging them.
# It's important to be precise here.
LEGITIMATE_DOMAINS = {
    "facebook": ["facebook.com", "m.facebook.com", "fb.com", "messenger.com"],
    "instagram": ["instagram.com", "instagr.am"],
    "whatsapp": ["whatsapp.com", "wa.me"],
    "tiktok": ["tiktok.com"],
    "tinder": ["tinder.com", "gotinder.com"],
    "snapchat": ["snapchat.com"],
    "wechat": ["wechat.com"],
    "telegram": ["telegram.org", "t.me"],
    "twitter": ["twitter.com", "x.com"],
    "pinterest": ["pinterest.com"],
    "linkedin": ["linkedin.com"],
    "line": ["line.me"],
    "discord": ["discord.com", "discord.gg"],
    "teams": ["teams.microsoft.com", "microsoft.com"],
    "zoom": ["zoom.us"],
    "amazon": ["amazon.com"],
    "alibaba": ["alibaba.com"],
    "youtube": ["youtube.com", "youtu.be"],
    "skype": ["skype.com"],
    "vk": ["vk.com"],
    "reddit": ["reddit.com", "old.reddit.com"],
    "email": [],
    "viber": ["viber.com"],
    "signal": ["signal.org"],
    "badoo": ["badoo.com"],
    "binance": ["binance.com"],
    "sharechat": ["sharechat.com"],
    "general": ["google.com"]
}


# --- Keyword Lists (case-insensitive matching will be applied) ---

# Keywords/phrases indicating urgency or pressure
URGENCY_KEYWORDS = [
    "urgent", "immediate action required", "act now", "limited time",
    "account suspended", "account will be closed", "final warning",
    "security alert", "unusual activity detected", "important notification",
    "don't delay", "expires soon", "offer ends today", "last chance",
    "your subscription will be cancelled", "payment declined"
]

# Keywords/phrases related to requests for sensitive information
SENSITIVE_INFO_KEYWORDS = [
    "verify your password", "confirm your password", "update your password",
    "password", "username", "login details", "credentials",
    "social security number", "ssn",
    "bank account", "account number", "routing number", "credit card number",
    "cvv", "pin number", "mother's maiden name", "security question",
    "confirm your details", "update your information", "verify your account",
    "provide your details", "personal information"
]

# Keywords/phrases indicating too-good-to-be-true offers, prizes, etc.
TOO_GOOD_TO_BE_TRUE_KEYWORDS = [
    "you have won", "you've won", "congratulations you won", "winner", "prize",
    "free gift", "claim your reward", "lottery", "sweepstakes",
    "guaranteed", "risk-free", "earn money fast", "work from home easy",
    "investment opportunity", "high return", "get rich quick",
    "inheritance", "unclaimed funds", "nigerian prince",
    "free followers", "pro account for free", "verified badge", # Social media specific
    "forex", "fx trading", "guaranteed profit", "trading signal", "forex robot",
    "metatrader", "mt4", "mt5", "copy trading", "pamm"
]

# Generic greetings/salutations that can be suspicious in unsolicited contexts
GENERIC_GREETINGS = [
    "dear customer", "dear user", "dear valued customer", "dear account holder",
    "dear friend", "hello sir/madam", "greetings"
]

# Keywords often found in tech support scams
TECH_SUPPORT_SCAM_KEYWORDS = [
    "microsoft support", "windows support", "apple support",
    "virus detected", "malware found", "your computer is infected",
    "call immediately", "technician", "remote access", "ip address compromised"
]

# Keywords related to payment requests or financial transactions
PAYMENT_KEYWORDS = [
    "payment", "invoice", "bill", "outstanding balance", "transfer funds",
    "wire transfer", "gift card", "cryptocurrency", "bitcoin", "western union", "moneygram",
    "urgent payment needed", "settle your account"
]


# --- Regular Expression Patterns ---

# Basic URL detection
URL_PATTERN = re.compile(
    r'(?:(?:https?|ftp):\/\/|www\.)'
    r'(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*'
    r'(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])',
    re.IGNORECASE
)

# Suspicious Top-Level Domains (TLDs)
SUSPICIOUS_TLDS = [
    '.xyz', '.top', '.loan', '.club', 'work', '.online', '.biz', '.info',
    '.icu', '.gq', '.cf', '.tk', '.ml',
    '.link', '.click', '.site', '.live', '.buzz', '.stream', '.download',
]

# Pattern for detecting strings that look like cryptocurrency addresses
CRYPTO_ADDRESS_PATTERNS = {
    "BTC": re.compile(r'\b(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{25,90})\b'),
    "ETH": re.compile(r'\b(0x[a-fA-F0-9]{40})\b'),
}

# Pattern for phone numbers
PHONE_NUMBER_PATTERN = re.compile(
    r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?(\d{3,4}[-.\s]?\d{3,4})'
)

# Suspicious URL Patterns
# These patterns aim to catch URLs that impersonate legitimate domains.
SUSPICIOUS_URL_PATTERNS = [
    # Impersonation using subdomains or hyphens
    r"https?://(?:[a-z0-9\-]+\.)*(?:facebook|fb|instagram|whatsapp|tiktok|tinder|snapchat|wechat|telegram|twitter|pinterest|linkedin|line|discord|teams|zoom|amazon|alibaba|youtube|skype|vk|reddit|viber|signal|badoo|binance|sharechat)\.com\.[a-z0-9\-]+\.[a-z]+",
    r"https?://(?:[a-z0-9\-]+\.)*(?:facebook|fb|instagram|whatsapp|tiktok|tinder|snapchat|wechat|telegram|twitter|pinterest|linkedin|line|discord|teams|zoom|amazon|alibaba|youtube|skype|vk|reddit|viber|signal|badoo|binance|sharechat)-[a-z0-9\-]+\.[a-z]+",
    # Common URL shorteners
    r"https?://bit\.ly",
    r"https?://goo\.gl",
    r"https?://t\.co",
    # IP Address URLs
    r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    # Generic suspicious keywords in the domain
    r"https?://[^/]*(?:login|secure|account|update|verify|support|admin)[^/]*\.(?:biz|info|tk|ml|ga|cf|gq|xyz|club|top|loan|work|online|site)",
    # Very long subdomains or many hyphens
    r"https?://(?:[a-z0-9\-]+\.){4,}",
    r"https?://[^/]*\-.*\-.*\-.*[a-z]+",
]


# --- Scoring Weights ---
HEURISTIC_WEIGHTS = {
    "URGENCY": 1.5,
    "SENSITIVE_INFO": 2.5,
    "TOO_GOOD_TO_BE_TRUE": 2.0,
    "GENERIC_GREETING": 0.5,
    "TECH_SUPPORT": 2.0,
    "PAYMENT_REQUEST": 1.5,
    "SUSPICIOUS_URL_KEYWORD": 1.0,
    "SUSPICIOUS_TLD": 2.0,
    "CRYPTO_ADDRESS": 2.5,
    "PHONE_NUMBER_UNSOLICITED": 1.0,
    "SUSPICIOUS_URL_PATTERN": 3.0, # High weight for matching a suspicious URL pattern
}

if __name__ == '__main__':
    print("--- Heuristic Definitions ---")
    # ... (rest of the test code can be added later)
