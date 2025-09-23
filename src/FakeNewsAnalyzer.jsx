import React, { useState } from 'react';

function FakeNewsAnalyzer() {
    const [url, setUrl] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = () => {
        setLoading(true);
        fetch('/analyze/fake-news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
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
            <h2>Fake News Analyzer</h2>
            <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter a news URL to analyze..."
                size="50"
            />
            <br />
            <button onClick={handleAnalyze} disabled={loading}>
                {loading ? 'Analyzing...' : 'Analyze'}
            </button>
            {result && (
                <div>
                    <h3>Analysis Results</h3>
                    {result.error ? (
                        <p>Error: {result.error}</p>
                    ) : (
                        <>
                            <p>Score: {result.score}</p>
                            <h4>Indicators Found:</h4>
                            <ul>
                                {result.indicators_found.map((indicator, index) => (
                                    <li key={index}>{indicator}</li>
                                ))}
                            </ul>
                            {result.named_entities && (
                                <>
                                    <h4>Named Entities Found:</h4>
                                    <h5>Organizations:</h5>
                                    <ul>
                                        {result.named_entities.organizations.map((org, index) => (
                                            <li key={index}>{org}</li>
                                        ))}
                                    </ul>
                                    <h5>Persons:</h5>
                                    <ul>
                                        {result.named_entities.persons.map((person, index) => (
                                            <li key={index}>{person}</li>
                                        ))}
                                    </ul>
                                </>
                            )}
                        </>
                    )}
                </div>
            )}
        </div>
    );
}

export default FakeNewsAnalyzer;
