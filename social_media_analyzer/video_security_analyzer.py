import re
from .heuristics import VIDEO_AI_KEYWORDS, DEEPFAKE_INDICATORS, HEURISTIC_WEIGHTS

def analyze_video_metadata(metadata_text):
    """
    Analyzes video metadata or description for indicators of AI generation or deepfakes.
    """
    if not metadata_text:
        return {"score": 0.0, "indicators_found": []}

    text_lower = metadata_text.lower()
    score = 0.0
    indicators_found = []

    # 1. Check for AI video keywords
    for keyword in VIDEO_AI_KEYWORDS:
        if keyword in text_lower:
            score += HEURISTIC_WEIGHTS.get("VIDEO_AI_KEYWORD", 2.0)
            indicators_found.append(f"Found AI video keyword: '{keyword}'")

    # 2. Check for mentions of deepfake indicators (if the user is describing the video)
    for indicator in DEEPFAKE_INDICATORS:
        if indicator in text_lower:
            score += HEURISTIC_WEIGHTS.get("DEEPFAKE_INDICATOR", 2.5)
            indicators_found.append(f"Metadata mentions potential deepfake indicator: '{indicator}'")

    # 3. Check for specific platform warnings (simulated)
    if "manipulated media" in text_lower or "synthetic content" in text_lower:
        score += 5.0
        indicators_found.append("Platform label for manipulated or synthetic media detected.")

    return {
        "score": round(score, 2),
        "indicators_found": indicators_found,
        "assessment": "High Risk" if score > 7.0 else "Elevated Risk" if score >= 4.0 else "Low Risk"
    }

def get_deepfake_checklist():
    """
    Returns a checklist of things to look for when verifying if a video is a deepfake.
    """
    return [
        {"id": "blinking", "label": "Does the person blink naturally? (Deepfakes often have irregular blinking)", "weight": 2.5},
        {"id": "lighting", "label": "Is the lighting on the face consistent with the background?", "weight": 2.0},
        {"id": "edges", "label": "Are there blurry edges around the face or hair?", "weight": 2.5},
        {"id": "audio_sync", "label": "Do the lip movements match the audio perfectly?", "weight": 3.0},
        {"id": "skin", "label": "Does the skin look too smooth or 'plastic'?", "weight": 1.5},
        {"id": "eyes", "label": "Do the eyes have natural reflections?", "weight": 2.0},
    ]
