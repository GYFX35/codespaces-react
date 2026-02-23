import re
import nltk
from .heuristics import (
    SENSATIONALIST_KEYWORDS,
    CLICKBAIT_PATTERNS,
    HEURISTIC_WEIGHTS
)

def _download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('help/tagsets')
    except LookupError:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    try:
        nltk.data.find('chunkers/maxent_ne_chunker')
    except LookupError:
        nltk.download('maxent_ne_chunker', quiet=True)
    try:
        nltk.data.find('corpora/words')
    except LookupError:
        nltk.download('words', quiet=True)

def analyze_text_for_fake_content(text):
    """
    Analyzes a block of text for indicators of fake or misleading content.
    """
    _download_nltk_data()
    if not text:
        return {"score": 0.0, "indicators_found": []}

    text_lower = text.lower()
    score = 0.0
    indicators_found = []

    # 1. Analyze text for sensationalist keywords
    for keyword in SENSATIONALIST_KEYWORDS:
        if keyword in text_lower:
            score += HEURISTIC_WEIGHTS.get("SENSATIONALIST_KEYWORD", 1.0)
            indicators_found.append(f"Found sensationalist keyword: '{keyword}'")

    # 2. Analyze text for clickbait patterns
    for pattern in CLICKBAIT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            score += HEURISTIC_WEIGHTS.get("CLICKBAIT_PATTERN", 1.5)
            indicators_found.append(f"Found clickbait pattern: '{pattern}'")

    # 3. Check for excessive punctuation (common in fake news/clickbait)
    if re.search(r'!!|!!\?|\?{2,}', text):
        score += 1.0
        indicators_found.append("Found excessive punctuation (e.g., '!!', '???').")

    # 4. Check for all caps words (excluding short acronyms)
    all_caps_words = re.findall(r'\b[A-Z]{4,}\b', text)
    if len(all_caps_words) >= 2:
        score += 1.0
        indicators_found.append(f"Found multiple words in all caps: {', '.join(all_caps_words[:3])}...")

    # 5. Named Entity Extraction (Optional, for context)
    named_entities = {"organizations": [], "persons": []}
    try:
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.ne_chunk(tagged)
        for entity in entities:
            if isinstance(entity, nltk.Tree):
                entity_text = " ".join([word for word, tag in entity.leaves()])
                if entity.label() == 'ORGANIZATION':
                    if entity_text not in named_entities["organizations"]:
                        named_entities["organizations"].append(entity_text)
                elif entity.label() == 'PERSON':
                    if entity_text not in named_entities["persons"]:
                        named_entities["persons"].append(entity_text)
    except Exception:
        # NLTK might not be fully initialized or data missing
        pass

    return {
        "score": round(score, 2),
        "indicators_found": indicators_found,
        "named_entities": named_entities,
        "assessment": "High suspicion" if score > 5.0 else "Moderate suspicion" if score >= 3.0 else "Low suspicion"
    }
