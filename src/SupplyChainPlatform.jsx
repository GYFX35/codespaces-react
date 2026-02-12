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
  "EXW": "Ex Works: Buyer takes all risk from seller's door.",
  "FOB": "Free On Board: Seller covers costs until goods are on ship.",
  "CIF": "Cost, Insurance, and Freight: Seller pays to destination port.",
  "DDP": "Delivered Duty Paid: Seller covers all costs including taxes."
};

export default function SupplyChainPlatform() {
  const [activeTab, setActiveTab] = useState('twin');
  const [selectedTerm, setSelectedTerm] = useState('EXW');
  const [trackingId, setTrackingId] = useState('');
  const [aiStatus, setAiStatus] = useState('Idle');
  const [blockchainLog, setBlockchainLog] = useState([]);

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

  return (
    <div className="supply-chain-container" style={{ color: 'white', textAlign: 'left', padding: '20px' }}>
      <h2>Supply Chain & Digital Twin Platform</h2>

      <div className="tabs" style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button onClick={() => setActiveTab('twin')}>Digital Twin (3D)</button>
        <button onClick={() => setActiveTab('incoterms')}>Incoterms</button>
        <button onClick={() => setActiveTab('logistics')}>Logistics AI</button>
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
          <select
            value={selectedTerm}
            onChange={(e) => setSelectedTerm(e.target.value)}
            style={{ padding: '10px', borderRadius: '5px', width: '100%', marginBottom: '20px' }}
          >
            {Object.keys(INCOTERMS_DATA).map(term => (
              <option key={term} value={term}>{term}</option>
            ))}
          </select>
          <div style={{ padding: '20px', border: '1px solid #444', borderRadius: '5px' }}>
            <strong>{selectedTerm}:</strong> {INCOTERMS_DATA[selectedTerm]}
          </div>
        </div>
      )}

      {activeTab === 'logistics' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div style={{ background: '#222', padding: '20px', borderRadius: '10px' }}>
            <h3>Logistics Optimizer</h3>
            <input
              type="text"
              placeholder="Enter Tracking ID (e.g. SHIP-123)"
              value={trackingId}
              onChange={(e) => setTrackingId(e.target.value)}
              style={{ padding: '10px', width: '80%', marginBottom: '10px' }}
            />
            <button onClick={runAIPrediction} style={{ display: 'block' }}>Run AI Analysis</button>
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

      <footer style={{ marginTop: '30px', fontSize: '12px', color: '#666' }}>
        Supply Chain AI Services Software v1.0.0 | Integrated with Digital Twin & Web3 Ledger.
      </footer>
    </div>
  );
}
