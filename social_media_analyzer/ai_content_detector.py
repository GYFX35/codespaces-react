import re
from .heuristics import AI_PHRASES, HEURISTIC_WEIGHTS

def analyze_text_for_ai_content(text):
    """
    Analyzes text for indicators of being AI-generated.
    """
    if not text:
        return {"score": 0.0, "indicators_found": [], "is_ai_generated": False}

    text_lower = text.lower()
    score = 0.0
    indicators_found = []

    # 1. Check for known AI phrases
    for phrase in AI_PHRASES:
        if phrase in text_lower:
            score += HEURISTIC_WEIGHTS.get("AI_PHRASE", 2.0)
            indicators_found.append(f"Found AI-typical phrase: '{phrase}'")

    # 2. Check for robotic structure (e.g., numbered lists with consistent formatting)
    numbered_list_pattern = r'\n\d+\.\s'
    numbered_lists = re.findall(numbered_list_pattern, text)
    if len(numbered_lists) >= 3:
        score += HEURISTIC_WEIGHTS.get("ROBOTIC_STRUCTURE", 3.0)
        indicators_found.append("Contains multiple numbered lists, typical of structured AI output.")

    # 3. Check for lack of common human errors (very basic check)
    # This is a heuristic: AI text is often too "perfect"
    # We could count common typos and if they are 0 in a long text, it's slightly more suspicious
    common_typos = ['teh', 'receive', 'believe', 'occured', 'definately']
    words = text_lower.split()
    if len(words) > 50:
        typo_found = False
        for word in words:
            if word in common_typos:
                typo_found = True
                break
        if not typo_found:
            score += HEURISTIC_WEIGHTS.get("LACK_OF_ERRORS", 1.5)
            indicators_found.append("Text is highly polished with no common human typos in a long passage.")

    # 4. Check for repetitive sentence starts
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) >= 5:
        starts = [s.split()[0].lower() if s.split() else "" for s in sentences]
        from collections import Counter
        counts = Counter(starts)
        most_common = counts.most_common(1)
        if most_common and most_common[0][1] / len(sentences) > 0.4:
            score += HEURISTIC_WEIGHTS.get("ROBOTIC_STRUCTURE", 3.0)
            indicators_found.append(f"High repetition of sentence starters ('{most_common[0][0]}'), suggests robotic generation.")

    is_ai = score >= 5.0

    return {
        "score": round(score, 2),
        "indicators_found": indicators_found,
        "is_ai_generated": is_ai,
        "assessment": "High likelihood" if score > 7.0 else "Medium likelihood" if score >= 5.0 else "Low likelihood"
    }
