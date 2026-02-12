import React, { useState, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { XR, ARButton, Controllers, Hands } from '@react-three/xr';
import { OrbitControls, Text, Sky, ContactShadows, Environment, Float, Box } from '@react-three/drei';
import * as THREE from 'three';
import { ethers } from 'ethers';

// --- Components ---

// Digital Twin: Warehouse / Cargo Box
function CargoBox({ position, color, speed = 0.01 }) {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  useFrame((state) => {
    if (meshRef.current) {
      // Move box back and forth to simulate movement in a warehouse
      meshRef.current.position.z += speed * Math.sin(state.clock.elapsedTime);
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
      <Box
        ref={meshRef}
        position={position}
        args={[0.5, 0.5, 0.5]}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <meshStandardMaterial color={hovered ? 'orange' : color} />
      </Box>
    </Float>
  );
}

// Digital Twin: Warehouse Floor
function Warehouse() {
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[20, 20]} />
        <meshStandardMaterial color="#222" />
      </mesh>
      <gridHelper args={[20, 20, 0xffffff, 0x444444]} rotation={[-Math.PI / 2, 0, 0]} />

      {/* Some shelving units simulated by boxes */}
      <Box position={[-2, 0.5, -2]} args={[1, 1, 4]}>
        <meshStandardMaterial color="#555" />
      </Box>
      <Box position={[2, 0.5, -2]} args={[1, 1, 4]}>
        <meshStandardMaterial color="#555" />
      </Box>

      {/* Moving Cargo */}
      <CargoBox position={[-1, 0.5, 0]} color="#8B4513" speed={0.02} />
      <CargoBox position={[1, 0.5, -1]} color="#CD853F" speed={0.015} />
      <CargoBox position={[0, 0.5, -2]} color="#DEB887" speed={0.01} />
    </group>
  );
}

// --- Main Component ---

const INCOTERMS_DATA = {
  "EXW": {
    "desc": "Ex Works: Buyer takes all risk from seller's door.",
    "risk": "Seller's premises",
    "cost": "Seller's premises",
    "modes": "Any"
  },
  "FCA": {
    "desc": "Free Carrier: Seller delivers to carrier at named place.",
    "risk": "Delivery to carrier",
    "cost": "Delivery to carrier",
    "modes": "Any"
  },
  "FOB": {
    "desc": "Free On Board: Seller covers costs until goods are on ship.",
    "risk": "On board vessel",
    "cost": "On board vessel",
    "modes": "Sea/Inland Waterway"
  },
  "CIF": {
    "desc": "Cost, Insurance, and Freight: Seller pays to destination port.",
    "risk": "On board vessel",
    "cost": "Destination port",
    "modes": "Sea/Inland Waterway"
  },
  "DAP": {
    "desc": "Delivered at Place: Seller delivers at named destination.",
    "risk": "At destination (ready for unloading)",
    "cost": "At destination (ready for unloading)",
    "modes": "Any"
  },
  "DDP": {
    "desc": "Delivered Duty Paid: Seller covers all costs including taxes.",
    "risk": "At destination (ready for unloading)",
    "cost": "At destination (cleared for import)",
    "modes": "Any"
  }
};

export default function SupplyChainPlatform() {
  const [activeTab, setActiveTab] = useState('twin');
  const [selectedTerm, setSelectedTerm] = useState('EXW');
  const [trackingId, setTrackingId] = useState('');
  const [aiStatus, setAiStatus] = useState('Idle');
  const [blockchainLog, setBlockchainLog] = useState([]);
  const [pipelineStep, setPipelineStep] = useState(0);
  const [securityScan, setSecurityScan] = useState(null);

  const logToBlockchain = async (event) => {
    setAiStatus('Securing data on blockchain...');
    // Simulate ethers interaction
    const hash = ethers.id(event + Date.now());
    const newLog = { event, hash: hash.substring(0, 16) + '...', time: new Date().toLocaleTimeString() };
    setBlockchainLog([newLog, ...blockchainLog].slice(0, 5));
    await new Promise(r => setTimeout(r, 800));
    setAiStatus('Data Verified.');
  };

  const runAIPrediction = () => {
    setAiStatus('AI Analyzing supply chain routes...');
    setTimeout(() => {
      setAiStatus('Optimal route found: Route A-7 via Singapore. Delay Probability: 5%.');
      logToBlockchain('Route Optimization Run');
    }, 1500);
  };

  const runDataPipeline = () => {
    setPipelineStep(1);
    const steps = [
      'Ingesting IoT Telemetry...',
      'Cleaning Data...',
      'Running AI Transformers...',
      'Loading to Warehouse...'
    ];
    let i = 0;
    const interval = setInterval(() => {
      if (i < steps.length) {
        setAiStatus(steps[i]);
        setPipelineStep(i + 1);
        i++;
      } else {
        clearInterval(interval);
        setAiStatus('Pipeline Complete.');
        logToBlockchain('Data Pipeline Executed');
      }
    }, 800);
  };

  const runSecurityScan = () => {
    setAiStatus('Scanning for anomalies...');
    setTimeout(() => {
      setSecurityScan({
        anomaly: "CRITICAL: Route deviation 22% detected near high-risk zone.",
        iotRisk: "MEDIUM: 3 sensors running outdated firmware.",
        fraud: "CLEAN: All invoices verified for this shipment."
      });
      setAiStatus('Security Scan Complete.');
      logToBlockchain('Security Audit Triggered');
    }, 2000);
  };

  return (
    <div className="supply-chain-container" style={{ color: 'white', textAlign: 'left', padding: '20px', fontFamily: 'sans-serif' }}>
      <header style={{ borderBottom: '1px solid #444', marginBottom: '20px', paddingBottom: '10px' }}>
        <h2 style={{ margin: 0 }}>Supply Chain & Logistics AI Platform</h2>
        <small style={{ color: '#888' }}>Enhanced Data Engineering & Security Integration</small>
      </header>

      <div className="tabs" style={{ marginBottom: '20px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button style={btnStyle(activeTab === 'twin')} onClick={() => setActiveTab('twin')}>Digital Twin (3D)</button>
        <button style={btnStyle(activeTab === 'incoterms')} onClick={() => setActiveTab('incoterms')}>Incoterms</button>
        <button style={btnStyle(activeTab === 'logistics')} onClick={() => setActiveTab('logistics')}>Logistics AI</button>
        <button style={btnStyle(activeTab === 'security')} onClick={() => setActiveTab('security')}>Security & Risk</button>
        <button style={btnStyle(activeTab === 'data')} onClick={() => setActiveTab('data')}>Data Engineering</button>
      </div>

      {activeTab === 'twin' && (
        <div style={{ width: '100%', height: '500px', background: '#000', borderRadius: '10px', overflow: 'hidden', position: 'relative' }}>
          <ARButton />
          <Canvas shadows camera={{ position: [5, 5, 5], fov: 50 }}>
            <XR>
              <Sky sunPosition={[100, 20, 100]} />
              <Environment preset="warehouse" />
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} castShadow />

              <Warehouse />

              <Text position={[0, 4, -5]} fontSize={0.5} color="white">
                Warehouse Digital Twin
              </Text>

              <Controllers />
              <Hands />
              <OrbitControls />
              <ContactShadows opacity={0.4} scale={20} blur={2} far={4.5} />
            </XR>
          </Canvas>
          <div style={{ position: 'absolute', bottom: 10, left: 10, background: 'rgba(0,0,0,0.6)', padding: '10px', fontSize: '12px' }}>
            Interactive 3D Simulation. Use mouse to rotate. Box movement simulates AGVs (Automated Guided Vehicles).
          </div>
        </div>
      )}

      {activeTab === 'incoterms' && (
        <div style={{ background: '#222', padding: '20px', borderRadius: '10px' }}>
          <h3>Incoterms 2020 Navigator</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px' }}>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {Object.keys(INCOTERMS_DATA).map(term => (
                <li
                  key={term}
                  onClick={() => setSelectedTerm(term)}
                  style={{
                    padding: '10px',
                    cursor: 'pointer',
                    background: selectedTerm === term ? '#444' : '#333',
                    marginBottom: '5px',
                    borderRadius: '4px'
                  }}
                >
                  {term} - {INCOTERMS_DATA[term].desc.split(':')[0]}
                </li>
              ))}
            </ul>
            <div style={{ padding: '20px', border: '1px solid #444', borderRadius: '5px', background: '#1a1a1a' }}>
              <h4 style={{ marginTop: 0, color: '#00ff00' }}>{selectedTerm} Details</h4>
              <p>{INCOTERMS_DATA[selectedTerm].desc}</p>
              <table style={{ width: '100%', fontSize: '14px', borderCollapse: 'collapse' }}>
                <tbody>
                  <tr style={{ borderBottom: '1px solid #333' }}><td style={{ padding: '8px' }}>Risk Transfer</td><td style={{ padding: '8px', color: '#aaa' }}>{INCOTERMS_DATA[selectedTerm].risk}</td></tr>
                  <tr style={{ borderBottom: '1px solid #333' }}><td style={{ padding: '8px' }}>Cost Transfer</td><td style={{ padding: '8px', color: '#aaa' }}>{INCOTERMS_DATA[selectedTerm].cost}</td></tr>
                  <tr><td style={{ padding: '8px' }}>Transport Modes</td><td style={{ padding: '8px', color: '#aaa' }}>{INCOTERMS_DATA[selectedTerm].modes}</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'logistics' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div style={{ background: '#222', padding: '20px', borderRadius: '10px' }}>
            <h3>Logistics Optimizer</h3>
            <p style={{ fontSize: '14px', color: '#aaa' }}>AI-driven route and delay prediction based on live environmental data.</p>
            <input
              type="text"
              placeholder="Enter Tracking ID (e.g. SHIP-123)"
              value={trackingId}
              onChange={(e) => setTrackingId(e.target.value)}
              style={{ padding: '10px', width: '80%', marginBottom: '10px', background: '#333', color: 'white', border: '1px solid #555' }}
            />
            <button onClick={runAIPrediction} style={{ display: 'block', padding: '10px 20px', background: '#007bff', border: 'none', color: 'white', borderRadius: '4px', cursor: 'pointer' }}>Run AI Analysis</button>
            <p style={{ marginTop: '20px', color: '#aaa' }}>Status: <span style={{ color: '#00ff00' }}>{aiStatus}</span></p>
          </div>

          <div style={{ background: '#222', padding: '20px', borderRadius: '10px' }}>
            <h3>Blockchain Audit Trail</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {blockchainLog.length === 0 && <li>No entries yet.</li>}
              {blockchainLog.map((log, i) => (
                <li key={i} style={{ fontSize: '12px', borderBottom: '1px solid #333', padding: '5px 0' }}>
                  [{log.time}] {log.event} <br/>
                  <small style={{ color: '#888' }}>Hash: {log.hash}</small>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {activeTab === 'security' && (
        <div style={{ background: '#222', padding: '20px', borderRadius: '10px' }}>
          <h3>AI Security & Risk Analyzer</h3>
          <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
            <button onClick={runSecurityScan} style={{ padding: '10px 20px', background: '#dc3545', border: 'none', color: 'white', borderRadius: '4px' }}>Perform Full Security Audit</button>
            <span style={{ alignSelf: 'center', color: '#aaa' }}>System Status: {aiStatus}</span>
          </div>

          {securityScan && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px' }}>
              <SecurityCard title="Shipment Anomaly" status="CRITICAL" desc={securityScan.anomaly} color="#ff4444" />
              <SecurityCard title="IoT Cyber Risk" status="MEDIUM" desc={securityScan.iotRisk} color="#ffbb33" />
              <SecurityCard title="Fraud Detection" status="SECURE" desc={securityScan.fraud} color="#00C851" />
            </div>
          )}
        </div>
      )}

      {activeTab === 'data' && (
        <div style={{ background: '#222', padding: '20px', borderRadius: '10px' }}>
          <h3>Data Engineering Pipeline</h3>
          <p style={{ fontSize: '14px', color: '#aaa' }}>Visualize the flow of telemetry from IoT edge devices to the analytics warehouse.</p>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '40px 0', padding: '20px', background: '#111', borderRadius: '8px' }}>
            <PipelineNode active={pipelineStep >= 1} label="IoT Ingestion" />
            <Arrow active={pipelineStep >= 1} />
            <PipelineNode active={pipelineStep >= 2} label="Cleaning" />
            <Arrow active={pipelineStep >= 2} />
            <PipelineNode active={pipelineStep >= 3} label="AI Transform" />
            <Arrow active={pipelineStep >= 3} />
            <PipelineNode active={pipelineStep >= 4} label="Data Warehouse" />
          </div>
          <button onClick={runDataPipeline} disabled={pipelineStep > 0 && pipelineStep < 4} style={{ padding: '10px 20px', background: '#28a745', border: 'none', color: 'white', borderRadius: '4px' }}>
            Trigger Pipeline Run
          </button>
        </div>
      )}

      <footer style={{ marginTop: '30px', fontSize: '12px', color: '#666', borderTop: '1px solid #333', paddingTop: '10px' }}>
        Supply Chain AI Services Software v1.2.0 | Integrated with Digital Twin, Web3 Ledger & AI Security.
      </footer>
    </div>
  );
}

// --- Helper Components ---

function btnStyle(active) {
  return {
    padding: '10px 15px',
    background: active ? '#444' : '#222',
    color: active ? '#00ff00' : 'white',
    border: '1px solid #555',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: active ? 'bold' : 'normal'
  };
}

function SecurityCard({ title, status, desc, color }) {
  return (
    <div style={{ border: `1px solid ${color}`, padding: '15px', borderRadius: '8px', background: 'rgba(255,255,255,0.05)' }}>
      <h4 style={{ margin: '0 0 10px 0', color: color }}>{title}</h4>
      <div style={{ fontSize: '12px', fontWeight: 'bold', marginBottom: '5px' }}>Status: {status}</div>
      <p style={{ fontSize: '13px', margin: 0, color: '#ccc' }}>{desc}</p>
    </div>
  );
}

function PipelineNode({ active, label }) {
  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{
        width: '60px',
        height: '60px',
        borderRadius: '50%',
        background: active ? '#00ff00' : '#333',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '0 auto 10px',
        boxShadow: active ? '0 0 15px #00ff00' : 'none',
        transition: 'all 0.5s ease'
      }}>
        {active ? '✅' : '⚙️'}
      </div>
      <span style={{ fontSize: '12px', color: active ? 'white' : '#666' }}>{label}</span>
    </div>
  );
}

function Arrow({ active }) {
  return (
    <div style={{ flex: 1, height: '2px', background: active ? '#00ff00' : '#333', margin: '0 10px', position: 'relative' }}>
      {active && <div style={{ position: 'absolute', right: 0, top: '-4px', border: '5px solid transparent', borderLeftColor: '#00ff00' }} />}
    </div>
  );
}
