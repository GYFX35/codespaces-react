import re
import urllib.request
from urllib.parse import urlparse
import nltk
from .heuristics import (
    FAKE_NEWS_DOMAINS,
    SENSATIONALIST_KEYWORDS,
    CLICKBAIT_PATTERNS,
    HEURISTIC_WEIGHTS
)

def analyze_url_for_fake_news(url):
    """
    Analyzes a URL for indicators of fake news.

    NOTE: This function requires the following NLTK data to be downloaded:
    - 'punkt'
    - 'averaged_perceptron_tagger'
    - 'maxent_ne_chunker'
    - 'words'
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    domain = urlparse(url).netloc.lower()

    score = 0.0
    indicators_found = []
    named_entities = {
        "organizations": [],
        "persons": [],
    }

    # 1. Check against known fake news domains
    if domain in FAKE_NEWS_DOMAINS:
        score += HEURISTIC_WEIGHTS.get("KNOWN_FAKE_NEWS_DOMAIN", 5.0)
        indicators_found.append(f"Domain '{domain}' is a known source of fake news.")
        return {
            "url": url,
            "score": round(score, 2),
            "indicators_found": indicators_found
        }

    # 2. Fetch and analyze content
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                html_content = response.read().decode('utf-8', errors='ignore')
                text_content = re.sub(r'<[^>]+>', '', html_content).lower()

                # 3. Analyze text for sensationalist keywords
                for keyword in SENSATIONALIST_KEYWORDS:
                    if keyword in text_content:
                        score += HEURISTIC_WEIGHTS.get("SENSATIONALIST_KEYWORD", 1.0)
                        indicators_found.append(f"Found sensationalist keyword: '{keyword}'")

                # 4. Analyze text for clickbait patterns
                for pattern in CLICKBAIT_PATTERNS:
                    if re.search(pattern, text_content, re.IGNORECASE):
                        score += HEURISTIC_WEIGHTS.get("CLICKBAIT_PATTERN", 1.5)
                        indicators_found.append(f"Found clickbait pattern: '{pattern}'")

                # 5. Named Entity Recognition
                tokens = nltk.word_tokenize(text_content)
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

            else:
                return {"error": f"Failed to fetch URL: HTTP status code {response.status}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

    return {
        "url": url,
        "score": round(score, 2),
        "indicators_found": indicators_found,
        "named_entities": named_entities
    }
