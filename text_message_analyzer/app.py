from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input, "text" field is required.'}), 400

    text_to_analyze = data['text']

    # Placeholder analysis logic
    is_suspicious = 'phishing' in text_to_analyze.lower()

    return jsonify({
        'text': text_to_analyze,
        'analysis': {
            'is_suspicious': is_suspicious
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
