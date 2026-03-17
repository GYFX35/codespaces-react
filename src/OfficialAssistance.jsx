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
  }
};

export default function OfficialAssistance() {
  const [activeRole, setActiveRole] = useState('police');

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
              <button className="action-btn" onClick={() => alert(`Launching ${tool.name}...`)}>Launch</button>
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
      `}</style>
    </div>
  );
}
