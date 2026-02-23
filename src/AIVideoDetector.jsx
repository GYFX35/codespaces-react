import React, { useState, useEffect } from 'react';

function AIVideoDetector() {
    const [metadata, setMetadata] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [checklist, setChecklist] = useState([]);
    const [checkedItems, setCheckedItems] = useState({});
    const [manualScore, setManualScore] = useState(0);

    useEffect(() => {
        fetch('/analyze/video-checklist')
            .then(res => res.json())
            .then(data => setChecklist(data))
            .catch(err => console.error("Error fetching checklist:", err));
    }, []);

    const handleAnalyzeMetadata = () => {
        setLoading(true);
        fetch('/analyze/ai-video', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ metadata }),
        })
            .then(res => res.json())
            .then(data => {
                setResult(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error:', error);
                setLoading(false);
            });
    };

    const handleCheckChange = (id, weight) => {
        const newChecked = { ...checkedItems, [id]: !checkedItems[id] };
        setCheckedItems(newChecked);

        let newScore = 0;
        checklist.forEach(item => {
            if (newChecked[item.id]) {
                newScore += item.weight;
            }
        });
        setManualScore(newScore);
    };

    return (
        <div className="analyzer-container">
            <h2>AI Video & Deepfake Security Detector</h2>

            <div className="section">
                <h3>Step 1: Metadata & Description Analysis</h3>
                <p>Paste the video description, tags, or any metadata available.</p>
                <textarea
                    value={metadata}
                    onChange={(e) => setMetadata(e.target.value)}
                    placeholder="Paste video metadata or description here..."
                    rows="5"
                    style={{ width: '100%', marginBottom: '10px' }}
                />
                <button onClick={handleAnalyzeMetadata} disabled={loading || !metadata}>
                    {loading ? 'Analyzing...' : 'Analyze Metadata'}
                </button>
                {result && (
                    <div className="results">
                        <p><strong>Assessment:</strong> {result.assessment}</p>
                        <p><strong>Risk Score:</strong> {result.score}</p>
                        {result.indicators_found.length > 0 && (
                            <ul>
                                {result.indicators_found.map((ind, i) => <li key={i}>{ind}</li>)}
                            </ul>
                        )}
                    </div>
                )}
            </div>

            <hr />

            <div className="section">
                <h3>Step 2: Manual Visual Inspection</h3>
                <p>Watch the video carefully and check any indicators you observe:</p>
                <div style={{ textAlign: 'left', display: 'inline-block', margin: '10px 0' }}>
                    {checklist.map(item => (
                        <div key={item.id} style={{ marginBottom: '8px' }}>
                            <label>
                                <input
                                    type="checkbox"
                                    checked={!!checkedItems[item.id]}
                                    onChange={() => handleCheckChange(item.id, item.weight)}
                                />
                                {item.label}
                            </label>
                        </div>
                    ))}
                </div>
                <div className="results" style={{ marginTop: '10px' }}>
                    <p><strong>Manual Observation Score:</strong> {manualScore.toFixed(1)}</p>
                    <p><strong>Visual Assessment:</strong> {
                        manualScore > 5 ? "High Likelihood of Manipulation" :
                        manualScore > 2 ? "Suspicious - Exercise Caution" : "Low Visual Indicators Found"
                    }</p>
                </div>
            </div>
        </div>
    );
}

export default AIVideoDetector;
