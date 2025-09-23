import React, { useState } from 'react';

function ScamAnalyzer() {
    const [text, setText] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = () => {
        setLoading(true);
        fetch('/analyze/scam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        })
            .then((res) => res.json())
            .then((data) => {
                setResult(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error:', error);
                setLoading(false);
            });
    };

    return (
        <div>
            <h2>Scam Analyzer</h2>
            <textarea
                rows="10"
                cols="50"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste a message to analyze for scams..."
            />
            <br />
            <button onClick={handleAnalyze} disabled={loading}>
                {loading ? 'Analyzing...' : 'Analyze'}
            </button>
            {result && (
                <div>
                    <h3>Analysis Results</h3>
                    <p>Score: {result.score}</p>
                    <h4>Indicators Found:</h4>
                    <ul>
                        {result.indicators_found.map((indicator, index) => (
                            <li key={index}>{indicator}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default ScamAnalyzer;
