import React, { useState } from 'react';

const assistanceRoles = {
  police: {
    title: 'Police Assistance',
    icon: '👮',
    description: 'Civilian law enforcement and public safety services.',
    tools: [
      { id: 'dispatch', name: 'Emergency Dispatch', icon: '📞', desc: 'Real-time coordination of emergency responses.' },
      { id: 'reporting', name: 'Incident Reporting', icon: '📝', desc: 'Secure portal for filing and tracking crime reports.' },
      { id: 'forensics', name: 'Forensic Analysis', icon: '🔬', desc: 'AI-assisted analysis of digital and physical evidence.' }
    ]
  },
  military: {
    title: 'Military Assistance',
    icon: '🪖',
    description: 'National defense and strategic security operations.',
    tools: [
      { id: 'dashboard', name: 'Strategic Dashboard', icon: '📊', desc: 'Global threat monitoring and resource allocation.' },
      { id: 'recon', name: 'Reconnaissance AI', icon: '🛰️', desc: 'Satellite and drone data processing for situational awareness.' },
      { id: 'comms', name: 'Tactical Comms', icon: '📡', desc: 'Encrypted communication channels for field operations.' }
    ]
  },
  gendarmery: {
    title: 'Gendarmerie Assistance',
    icon: '🛡️',
    description: 'Military-force law enforcement for territorial and specialized security.',
    tools: [
      { id: 'territory', name: 'Territorial Security', icon: '🗺️', desc: 'Regional patrol management and community safety.' },
      { id: 'traffic', name: 'Traffic Management', icon: '🚦', desc: 'Coordination of road safety and major transit routes.' },
      { id: 'response', name: 'Specialized Response', icon: '🚨', desc: 'Elite units for counter-terrorism and high-risk interventions.' }
    ]
  },
  opsec: {
    title: 'Operational Security',
    icon: '🔐',
    description: 'Cloud, IoT, and AI-driven security operations for modern infrastructure.',
    tools: [
      {
        id: 'cloud_guard',
        name: 'Cloud Guard',
        icon: '☁️',
        desc: 'AI scanner for leaked credentials and sensitive cloud data.',
        endpoint: '/analyze/cloud',
        getPayload: () => ({ content: "Cloud scan simulation with fake AWS key: AKIA0000000000000000 and fake Google API Key: AIza00000000000000000000000000000000000" })
      },
      {
        id: 'iot_shield',
        name: 'IoT Shield',
        icon: '🌐',
        desc: 'Real-time anomaly detection for industrial IoT networks.',
        endpoint: '/analyze/iot',
        getPayload: () => ({ device_data: { voltage: 2.6, temperature: 82, rssi: -95 } })
      },
      {
        id: 'opsec_analyzer',
        name: 'OpSec Analyzer',
        icon: '🕵️',
        desc: 'AI-driven analysis of operational logs for procedural threats.',
        endpoint: '/analyze/opsec',
        getPayload: () => ({ logs: ["unauthorized access attempt", "nmap scan detected", "large outbound transfer", "sudo usage"] })
      }
    ]
  }
};

export default function OfficialAssistance() {
  const [activeRole, setActiveRole] = useState('police');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLaunch = async (tool) => {
    if (!tool.endpoint) {
      alert(`Launching ${tool.name}... (Simulation mode)`);
      return;
    }

    setLoading(true);
    setAnalysisResult(null);

    try {
      const response = await fetch(tool.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tool.getPayload())
      });

      const data = await response.json();
      setAnalysisResult({ title: tool.name, data });
    } catch (error) {
      console.error("Error launching tool:", error);
      alert("Failed to connect to security backend. Make sure the Flask server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="assistance-container">
      <div className="role-selector">
        {Object.entries(assistanceRoles).map(([id, role]) => (
          <button
            key={id}
            className={`role-tab ${activeRole === id ? 'active' : ''}`}
            onClick={() => setActiveRole(id)}
          >
            <span className="role-icon">{role.icon}</span>
            {role.title}
          </button>
        ))}
      </div>

      <div className="role-content">
        <h2>{assistanceRoles[activeRole].title}</h2>
        <p className="role-description">{assistanceRoles[activeRole].description}</p>

        <div className="tool-list">
          {assistanceRoles[activeRole].tools.map((tool) => (
            <div key={tool.id} className="assistance-tool-card">
              <div className="tool-icon">{tool.icon}</div>
              <div className="tool-info">
                <h3>{tool.name}</h3>
                <p>{tool.desc}</p>
              </div>
              <button
                className="action-btn"
                onClick={() => handleLaunch(tool)}
                disabled={loading}
              >
                {loading ? 'Processing...' : 'Launch'}
              </button>
            </div>
          ))}
        </div>

        {analysisResult && (
          <div className="analysis-result">
            <h3>{analysisResult.title} - AI Analysis Output</h3>
            <pre>{JSON.stringify(analysisResult.data, null, 2)}</pre>
            <button className="close-result" onClick={() => setAnalysisResult(null)}>Close Results</button>
          </div>
        )}
      </div>

      <style jsx>{`
        .assistance-container {
          padding: 20px;
          max-width: 1000px;
          margin: 0 auto;
          color: white;
        }
        .role-selector {
          display: flex;
          gap: 10px;
          margin-bottom: 30px;
          border-bottom: 1px solid #444;
          padding-bottom: 10px;
        }
        .role-tab {
          background: #333;
          border: 1px solid #555;
          color: white;
          padding: 10px 20px;
          border-radius: 8px 8px 0 0;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 10px;
          font-weight: bold;
          transition: background 0.2s;
        }
        .role-tab.active {
          background: #61dafb;
          color: #282c34;
          border-color: #61dafb;
        }
        .role-content {
          background: #282c34;
          padding: 30px;
          border-radius: 0 0 12px 12px;
          border: 1px solid #444;
          border-top: none;
        }
        .role-description {
          color: #aaa;
          margin-bottom: 30px;
          font-style: italic;
        }
        .tool-list {
          display: grid;
          grid-template-columns: 1fr;
          gap: 15px;
        }
        .assistance-tool-card {
          display: flex;
          align-items: center;
          background: #333;
          padding: 20px;
          border-radius: 10px;
          gap: 20px;
        }
        .tool-icon {
          font-size: 2.5rem;
        }
        .tool-info {
          flex-grow: 1;
        }
        .tool-info h3 {
          margin: 0 0 5px 0;
          color: #61dafb;
        }
        .tool-info p {
          margin: 0;
          color: #ccc;
          font-size: 0.9rem;
        }
        .action-btn {
          background: #61dafb;
          color: #282c34;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
          font-weight: bold;
          cursor: pointer;
        }
        .action-btn:disabled {
          background: #555;
          cursor: not-allowed;
        }
        .analysis-result {
          margin-top: 30px;
          background: #1e2127;
          padding: 20px;
          border-radius: 8px;
          border: 1px solid #61dafb;
        }
        .analysis-result pre {
          background: #000;
          padding: 15px;
          border-radius: 5px;
          overflow-x: auto;
          color: #00ff00;
          font-family: 'Courier New', Courier, monospace;
          font-size: 0.85rem;
        }
        .close-result {
          background: transparent;
          color: #61dafb;
          border: 1px solid #61dafb;
          padding: 5px 15px;
          border-radius: 4px;
          cursor: pointer;
          margin-top: 10px;
        }
      `}</style>
    </div>
  );
}
