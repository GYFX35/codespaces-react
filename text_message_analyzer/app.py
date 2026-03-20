from flask import Flask, request, jsonify
from social_media_analyzer import (
    scam_detector,
    fake_news_detector,
    ai_content_detector,
    fake_content_verifier,
    operational_security
)
import os

app = Flask(__name__)

def get_api_key():
    """Gets the Google API key from environment variables."""
    return os.environ.get("GOOGLE_API_KEY")

@app.route('/analyze/scam', methods=['POST'])
def analyze_scam():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text_to_analyze = data['text']
    api_key = get_api_key()

    result = scam_detector.analyze_text_for_scams(text_to_analyze, api_key=api_key)
    return jsonify(result)

@app.route('/analyze/fake-news', methods=['POST'])
def analyze_fake_news():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    url_to_analyze = data['url']

    result = fake_news_detector.analyze_url_for_fake_news(url_to_analyze)
    return jsonify(result)

@app.route('/analyze/ai-content', methods=['POST'])
def analyze_ai_content():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text_to_analyze = data['text']
    result = ai_content_detector.analyze_text_for_ai_content(text_to_analyze)
    return jsonify(result)

@app.route('/analyze/fake-content', methods=['POST'])
def analyze_fake_content():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text_to_analyze = data['text']
    result = fake_content_verifier.analyze_text_for_fake_content(text_to_analyze)
    return jsonify(result)

@app.route('/analyze/cloud', methods=['POST'])
def analyze_cloud():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Missing 'content' in request body"}), 400

    content = data['content']
    result = operational_security.analyze_cloud_security(content)
    return jsonify(result)

@app.route('/analyze/iot', methods=['POST'])
def analyze_iot():
    data = request.get_json()
    if not data or 'device_data' not in data:
        return jsonify({"error": "Missing 'device_data' in request body"}), 400

    device_data = data['device_data']
    result = operational_security.analyze_iot_security(device_data)
    return jsonify(result)

@app.route('/analyze/opsec', methods=['POST'])
def analyze_opsec():
    data = request.get_json()
    if not data or 'logs' not in data:
        return jsonify({"error": "Missing 'logs' in request body"}), 400

    logs = data['logs']
    result = operational_security.analyze_opsec_security(logs)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
