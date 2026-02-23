import React, { useState } from 'react';

function FakeContentAnalyzer() {
    const [text, setText] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = () => {
        setLoading(true);
        fetch('/analyze/fake-content', {
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
        <div className="analyzer-container">
            <h2>Fake Content Verifier</h2>
            <p>Paste text content (e.g., a social media post or article snippet) to check for misleading indicators.</p>
            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste content here..."
                rows="10"
                style={{ width: '100%', marginBottom: '10px' }}
            />
            <br />
            <button onClick={handleAnalyze} disabled={loading || !text}>
                {loading ? 'Analyzing...' : 'Verify Content'}
            </button>
            {result && (
                <div className="results">
                    <h3>Analysis Results</h3>
                    <p><strong>Assessment:</strong> {result.assessment}</p>
                    <p><strong>Suspicion Score:</strong> {result.score}</p>
                    {result.indicators_found.length > 0 && (
                        <>
                            <h4>Indicators Found:</h4>
                            <ul>
                                {result.indicators_found.map((indicator, index) => (
                                    <li key={index}>{indicator}</li>
                                ))}
                            </ul>
                        </>
                    )}
                    {result.named_entities && (result.named_entities.organizations.length > 0 || result.named_entities.persons.length > 0) && (
                        <div className="entities">
                            <h4>Entities Mentioned:</h4>
                            {result.named_entities.organizations.length > 0 && (
                                <p><strong>Organizations:</strong> {result.named_entities.organizations.join(', ')}</p>
                            )}
                            {result.named_entities.persons.length > 0 && (
                                <p><strong>People:</strong> {result.named_entities.persons.join(', ')}</p>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default FakeContentAnalyzer;
