# This file makes 'scam_detector' a Python package.

# Expose constants and potentially functions if needed by other modules directly
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
    HEURISTIC_WEIGHTS
)

from .analyzer import analyze_text_for_scams
