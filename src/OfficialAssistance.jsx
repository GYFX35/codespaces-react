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
  mobile_operator: {
    title: 'Mobile Operator',
    icon: '📱',
    description: 'Telecommunications security, IoT protection, and prevention of internet data theft.',
    tools: [
      { id: 'iot_audit', name: 'IoT Security Audit', icon: '🤖', desc: 'Scan connected IoT devices for vulnerabilities and unauthorized access.' },
      { id: 'anti_stealing', name: 'Anti-Stealing Guard', icon: '🔒', desc: 'Detect and prevent bandwidth or data theft from mobile networks.' },
      { id: 'signal_integrity', name: 'Signal Integrity', icon: '📶', desc: 'Monitor network signal strength and detect interference or spoofing.' }
    ]
  },
  operational_security: {
    title: 'Operational Security',
    icon: '🕵️',
    description: 'AI-driven security auditing for cloud, IoT, and operational logs.',
    tools: [
      { id: 'cloud_audit', name: 'Cloud Security Audit', icon: '☁️', desc: 'Scan cloud configurations for misconfigurations and exposure.' },
      { id: 'iot_telemetry', name: 'IoT Telemetry Analysis', icon: '📡', desc: 'Real-time analysis of IoT device telemetry for anomalies.' },
      { id: 'opsec_scanner', name: 'OpSec Log Scanner', icon: '📜', desc: 'Audit operational logs for sensitive data leaks and security threats.' }
    ]
  }
};

export default function OfficialAssistance() {
  const [activeRole, setActiveRole] = useState('police');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLaunch = async (tool) => {
    let endpoint = '';
    let payload = {};

    if (tool.id === 'cloud_audit') {
      endpoint = '/analyze/cloud';
      const config = prompt("Enter cloud configuration to audit:");
      if (!config) return;
      payload = { config };
    } else if (tool.id === 'iot_telemetry') {
      endpoint = '/analyze/iot';
      const voltage = prompt("Enter IoT voltage (V):", "3.3");
      const temperature = prompt("Enter IoT temperature (°C):", "25");
      if (voltage === null || temperature === null) return;
      payload = { voltage: parseFloat(voltage), temperature: parseFloat(temperature) };
    } else if (tool.id === 'opsec_scanner') {
      endpoint = '/analyze/opsec';
      const logs = prompt("Enter operational logs to scan:");
      if (!logs) return;
      payload = { logs };
    } else {
      alert(`Launching ${tool.name}... (Simulated)`);
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      setResult({ tool: tool.name, data });
    } catch (error) {
      console.error("Error launching tool:", error);
      alert("Failed to connect to the analysis backend.");
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

        {loading && <div className="loading-overlay">Analyzing...</div>}

        {result && (
          <div className="analysis-result-box">
            <h3>{result.tool} Results</h3>
            <div className={`status-badge ${result.data.status}`}>
              Status: {result.data.status}
            </div>
            <ul>
              {result.data.findings.map((finding, idx) => (
                <li key={idx}>{finding}</li>
              ))}
            </ul>
            <button className="close-btn" onClick={() => setResult(null)}>Close</button>
          </div>
        )}

        <div className="tool-list">
          {assistanceRoles[activeRole].tools.map((tool) => (
            <div key={tool.id} className="assistance-tool-card">
              <div className="tool-icon">{tool.icon}</div>
              <div className="tool-info">
                <h3>{tool.name}</h3>
                <p>{tool.desc}</p>
              </div>
              <button className="action-btn" onClick={() => handleLaunch(tool)}>Launch</button>
            </div>
          ))}
        </div>
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
        .analysis-result-box {
          background: #1e2127;
          border: 1px solid #61dafb;
          padding: 20px;
          border-radius: 10px;
          margin-bottom: 30px;
        }
        .status-badge {
          display: inline-block;
          padding: 5px 10px;
          border-radius: 4px;
          font-weight: bold;
          margin-bottom: 10px;
        }
        .status-badge.SECURE, .status-badge.STABLE, .status-badge.CLEAR { background: #4caf50; }
        .status-badge.RISK_DETECTED, .status-badge.ANOMALY, .status-badge.THREAT_DETECTED { background: #f44336; }
        .loading-overlay {
          padding: 20px;
          text-align: center;
          color: #61dafb;
          font-weight: bold;
        }
        .close-btn {
          background: #555;
          color: white;
          border: none;
          padding: 5px 15px;
          border-radius: 4px;
          cursor: pointer;
          margin-top: 10px;
        }
      `}</style>
    </div>
  );
}
