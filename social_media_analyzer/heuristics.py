import re

# --- Legitimate Domains ---
# This list helps the analyzer to recognize official domains and avoid flagging them.
# It's important to be precise here.
LEGITIMATE_DOMAINS = {
    "facebook": ["facebook.com", "m.facebook.com", "fb.com", "messenger.com"],
    "instagram": ["instagram.com", "instagr.am"],
    "whatsapp": ["whatsapp.com", "wa.me"],
    "tiktok": ["tiktok.com"],
    "douyin": ["douyin.com"],
    "kuaishou": ["kuaishou.com", "kwai.com", "kwai.net"],
    "tinder": ["tinder.com", "gotinder.com"],
    "snapchat": ["snapchat.com"],
    "wechat": ["wechat.com"],
    "telegram": ["telegram.org", "t.me"],
    "twitter": ["twitter.com", "x.com"],
    "pinterest": ["pinterest.com"],
    "linkedin": ["linkedin.com"],
    "line": ["line.me"],
    "messenger": ["messenger.com"],
    "musical.ly": ["musical.ly"],
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
    "qzone": ["qzone.qq.com"],
    "qq": ["qq.com"],
    "vimeo": ["vimeo.com"],
    "paypal": ["paypal.com", "paypal.me"],
    "stripe": ["stripe.com", "stripe.io"],
    "payoneer": ["payoneer.com"],
    "banks": [ # General list, can be expanded
        "bankofamerica.com", "chase.com", "wellsfargo.com", "citibank.com",
        "hsbc.com", "barclays.com", "deutsche-bank.com", "santander.com"
    ],
    "general": ["google.com"],
    "general_web": [
        "wikipedia.org", "yahoo.com", "live.com", "microsoft.com",
        "apple.com", "netflix.com", "twitch.tv", "ebay.com",
        "craigslist.org", "imdb.com", "nytimes.com", "theguardian.com",
        "bbc.com", "cnn.com", "espn.com", "walmart.com", "target.com",
        "bestbuy.com", "homedepot.com", "lowes.com", "costco.com",
        "stackoverflow.com", "github.com", "gitlab.com", "wordpress.org",
        "wordpress.com", "blogger.com", "tumblr.com", "medium.com",
        "quora.com", "flickr.com", "adobe.com", "soundcloud.com",
        "spotify.com", "dropbox.com", "box.com", "slack.com",
        "salesforce.com", "oracle.com", "sap.com", "ibm.com", "dell.com",
        "hp.com", "intel.com", "amd.com", "nvidia.com", "booking.com",
        "airbnb.com", "expedia.com", "tripadvisor.com", "fedex.com",
        "ups.com", "usps.com", "dhl.com"
    ]
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
    "urgent payment needed", "settle your account",
    # Fintech specific
    "paypal", "stripe", "payoneer", "cash app", "venmo", "zelle",
    # Bank transfer specific
    "bank transfer", "wire details", "account details", "iban", "swift code", "bic"
]

# --- Teenager Protection Heuristics ---

# Keywords/phrases related to cyberbullying
CYBERBULLYING_KEYWORDS = [
    "loser", "stupid", "idiot", "hate you", "ugly", "fat",
    "kill yourself", "kys", "go die", "nobody likes you", "freak",
    "weirdo", "everyone hates you", "you're worthless", "pathetic",
    "troll", "noob", "poser", "wannabe", "go away",
    "social reject", "outcast", "misfit", "dork", "nerd"
]

# Keywords/phrases related to inappropriate content (sexual, violent, etc.)
INAPPROPRIATE_CONTENT_KEYWORDS = [
    # Sexually suggestive
    "nude", "sexting", "send nudes", "horny", "slut", "whore", "dick", "pussy",
    "porn", "sexy pic", "private parts", "hook up",
    # Violence
    "kill", "murder", "blood", "gun", "knife", "fight me",
    "i will hurt you", "beat you up", "gonna get you",
    # Drugs/Alcohol
    "drugs", "weed", "cocaine", "pills", "get high", "drunk", "wasted"
]

# Keywords/phrases indicating oversharing of personal information
PRIVACY_RISK_KEYWORDS = [
    "my address is", "i live at", "my phone number is", "call me at",
    "my full name is", "my school is", "i go to [school_name]",
    "my mom's name is", "my dad's name is",
    "i'm home alone", "parents are out", "my password is"
]


# --- AI Content Heuristics ---

AI_PHRASES = [
    "as an ai language model",
    "based on the information provided",
    "it is important to note that",
    "in conclusion",
    "furthermore",
    "moreover",
    "on the other hand",
    "at the end of the day",
    "it is worth mentioning",
    "provide a comprehensive overview",
    "the content provided",
    "can be summarized as",
    "let me know if you need any further assistance",
    "here is a summary of",
]

# --- Video AI & Deepfake Heuristics ---

VIDEO_AI_KEYWORDS = [
    "deepfake", "ai-generated video", "synthetic media", "face swap",
    "avatar video", "digital human", "ai spokesperson", "lip-sync ai"
]

DEEPFAKE_INDICATORS = [
    "unnatural blinking",
    "inconsistent lighting on face",
    "blurred edges around face",
    "unnatural skin texture",
    "audio-visual sync issues",
    "robotic voice tonality",
    "strange reflections in eyes",
    "lack of micro-expressions",
    "distorted background when moving",
]

# --- Fake News Heuristics ---

FAKE_NEWS_DOMAINS = [
    "abcnews.com.co", "cnn.com.de", "daily-mail.com.de",
    "infowars.com", "naturalnews.com", "breitbart.com",
    "worldnewsdailyreport.com", "theonion.com", # The Onion is satire, but often mistaken for real news
    "yournewswire.com", "davidwolfe.com"
]

SENSATIONALIST_KEYWORDS = [
    "shocking", "bombshell", "secret", "cover-up",
    "miracle", "cure", "unbelievable", "outrageous",
    "conspiracy", "hidden truth", "what they don't want you to know", "fake news"
]

CLICKBAIT_PATTERNS = [
    r"you won't believe", r"will shock you", r"number \d will amaze you",
    r"this one weird trick", r"doctors hate him", r"the truth about",
    r"scientists baffled", r"what happened next", r"secret to",
    r"completely changed my life", r"instant results", r"limited time offer",
    r"everyone is talking about", r"gone viral"
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

# Pattern for detecting strings that look like financial identifiers
FINANCIAL_ADDRESS_PATTERNS = {
    "BTC": re.compile(r'\b(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{25,90})\b'),
    "ETH": re.compile(r'\b(0x[a-fA-F0-9]{40})\b'),
    "IBAN": re.compile(r'\b([A-Z]{2}\d{2}[A-Z0-9]{11,30})\b'),
    "SWIFT_BIC": re.compile(r'\b([A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)\b'),
}

# Pattern for phone numbers
PHONE_NUMBER_PATTERN = re.compile(
    r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?(\d{3,4}[-.\s]?\d{3,4})'
)

# Suspicious URL Patterns
# These patterns aim to catch URLs that impersonate legitimate domains.
def generate_suspicious_url_patterns(legitimate_domains):
    """
    Generates regex patterns to detect URLs impersonating legitimate domains.
    """
    all_service_keywords = set()
    for platform, domains in legitimate_domains.items():
        if platform not in ["general", "general_web", "banks"]:
            all_service_keywords.add(platform)
        for domain in domains:
            # Add the core part of the domain, e.g., "facebook" from "facebook.com"
            keyword = domain.split('.')[0]
            if keyword != "com" and len(keyword) > 2:
                all_service_keywords.add(keyword)

    # Remove very generic keywords that might cause false positives
    all_service_keywords -= {'google', 'apple', 'microsoft'}

    # Create a regex group of all keywords
    keyword_group = "|".join(re.escape(k) for k in sorted(list(all_service_keywords), key=len, reverse=True))

    patterns = [
        # Impersonation using subdomains or hyphens, e.g., "facebook.security-alert.com" or "facebook-login.com"
        # This now uses the dynamically generated keyword group
        r"https?://(?:[a-z0-9\-]+\.)*(?:" + keyword_group + r")\.(?:[a-z0-9\-]+)\.(?:[a-z]+)",
        r"https?://(?:[a-z0-9\-]+\.)*(?:" + keyword_group + r")-(?:[a-z0-9\-]+)\.(?:[a-z]+)",

        # Common URL shorteners
        r"https?://bit\.ly",
        r"https?://goo\.gl",
        r"https?://t\.co",
        # IP Address URLs
        r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        # Generic suspicious keywords in the domain combined with suspicious TLDs
        r"https?://[^/]*(?:login|secure|account|update|verify|support|admin)[^/]*\.(?:biz|info|tk|ml|ga|cf|gq|xyz|club|top|loan|work|online|site)",
        # Very long subdomains (potential phishing)
        r"https?://(?:[a-z0-9\-]+\.){4,}",
        # Multiple hyphens in the domain (potential phishing)
        r"https?://[^/]*\-.*\-.*\-.*[a-z]+",
    ]
    return patterns

SUSPICIOUS_URL_PATTERNS = generate_suspicious_url_patterns(LEGITIMATE_DOMAINS)


# --- Scoring Weights ---
HEURISTIC_WEIGHTS = {
    "KNOWN_FAKE_NEWS_DOMAIN": 5.0,
    "SENSATIONALIST_KEYWORD": 1.0,
    "CLICKBAIT_PATTERN": 1.5,
    "URGENCY": 1.5,
    "SENSITIVE_INFO": 2.5,
    "TOO_GOOD_TO_BE_TRUE": 2.0,
    "GENERIC_GREETING": 0.5,
    "TECH_SUPPORT": 2.0,
    "PAYMENT_REQUEST": 1.5,
    "SUSPICIOUS_URL_KEYWORD": 1.0,
    "SUSPICIOUS_TLD": 2.0,
    "BTC_ADDRESS": 2.5,
    "ETH_ADDRESS": 2.5,
    "IBAN_ADDRESS": 3.0,
    "SWIFT_BIC_ADDRESS": 3.0,
    "PHONE_NUMBER_UNSOLICITED": 1.0,
    "SUSPICIOUS_URL_PATTERN": 3.0, # High weight for matching a suspicious URL pattern
    "GOOGLE_SAFE_BROWSING_HIT": 10.0, # Very high weight for a positive Google Safe Browsing match
    "AI_PHRASE": 2.0,
    "ROBOTIC_STRUCTURE": 3.0,
    "LACK_OF_ERRORS": 1.5,
    "DEEPFAKE_INDICATOR": 2.5,
    "VIDEO_AI_KEYWORD": 2.0,
    # Teenager Protection Weights
    "CYBERBULLYING": 2.5,
    "INAPPROPRIATE_CONTENT": 3.0,
    "PRIVACY_RISK": 3.5,
}

if __name__ == '__main__':
    print("--- Heuristic Definitions ---")
    # ... (rest of the test code can be added later)
