from .heuristics import (
    CYBERBULLYING_KEYWORDS,
    INAPPROPRIATE_CONTENT_KEYWORDS,
    PRIVACY_RISK_KEYWORDS,
    HEURISTIC_WEIGHTS
)

def analyze_text_for_teen_risks(text, analysis_type):
    """
    Analyzes text for a specific type of risk to teenagers.

    :param text: The text content to analyze.
    :param analysis_type: The type of analysis to perform ('cyberbullying',
                          'inappropriate_content', 'privacy_risk').
    :return: A dictionary with the score and indicators found.
    """
    if not text:
        return {"score": 0.0, "indicators_found": []}

    text_lower = text.lower()
    score = 0.0
    indicators_found = []

    keyword_map = {
        'cyberbullying': ('CYBERBULLYING', CYBERBULLYING_KEYWORDS),
        'inappropriate_content': ('INAPPROPRIATE_CONTENT', INAPPROPRIATE_CONTENT_KEYWORDS),
        'privacy_risk': ('PRIVACY_RISK', PRIVACY_RISK_KEYWORDS),
    }

    if analysis_type not in keyword_map:
        return {"error": "Invalid analysis type specified."}

    category, keywords = keyword_map[analysis_type]
    weight = HEURISTIC_WEIGHTS.get(category.upper(), 1.0)

    for keyword in keywords:
        if keyword in text_lower:
            message = f"Detected potential {category.replace('_', ' ').lower()} keyword: '{keyword}'"
            if message not in indicators_found:
                indicators_found.append(message)
                score += weight

    return {
        "score": round(score, 2),
        "indicators_found": indicators_found
    }

def analyze_for_cyberbullying(text):
    """Analyzes text for signs of cyberbullying."""
    return analyze_text_for_teen_risks(text, 'cyberbullying')

def analyze_for_inappropriate_content(text):
    """Analyzes text for inappropriate content."""
    return analyze_text_for_teen_risks(text, 'inappropriate_content')

def analyze_for_privacy_risks(text):
    """Analyzes text for privacy risks (oversharing)."""
    return analyze_text_for_teen_risks(text, 'privacy_risk')