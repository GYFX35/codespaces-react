import React, { useState, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { XR, ARButton, VRButton, Interactive, Controllers, Hands } from '@react-three/xr';
import { OrbitControls, Text, Sky, ContactShadows, Environment } from '@react-three/drei';
import * as THREE from 'three';
import { ethers } from 'ethers';

// Mock Blockchain Service using Ethers.js
const BlockchainService = {
  logEvidence: async (evidenceId, metadata) => {
    console.log(`[Blockchain] Logging evidence: ${evidenceId}`, metadata);
    // Simulate blockchain delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Create a deterministic hash based on evidence and metadata
    const dataString = JSON.stringify({ evidenceId, metadata, salt: Math.random() });
    const hash = ethers.keccak256(ethers.toUtf8Bytes(dataString));

    return {
      hash: hash,
      timestamp: Date.now(),
      blockNumber: Math.floor(Math.random() * 1000000)
    };
  }
};

// Mock AI Service
const AIService = {
  analyzeEvidence: async (evidenceType) => {
    console.log(`[AI] Analyzing evidence: ${evidenceType}`);
    await new Promise(resolve => setTimeout(resolve, 1500));
    const analysis = {
      'gun': 'Weapon used in the crime. Fingerprints found: John Doe.',
      'laptop': 'Encrypted files found. Decoding suggests a heist plan.',
      'badge': 'Stolen FBI badge. Belongs to Agent Miller who went missing.'
    };
    return analysis[evidenceType] || 'Inconclusive evidence.';
  }
};

function Evidence({ position, type, onCollect }) {
  const [hovered, setHovered] = useState(false);
  const meshRef = useRef();

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.01;
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime) * 0.1;
    }
  });

  const getColor = () => {
    switch (type) {
      case 'gun': return 'red';
      case 'laptop': return 'blue';
      case 'badge': return 'gold';
      default: return 'gray';
    }
  };

  return (
    <Interactive onSelect={() => onCollect(type)}>
      <mesh
        ref={meshRef}
        position={position}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
        onClick={() => onCollect(type)}
      >
        {type === 'gun' && <boxGeometry args={[0.2, 0.4, 0.1]} />}
        {type === 'laptop' && <boxGeometry args={[0.4, 0.05, 0.3]} />}
        {type === 'badge' && <sphereGeometry args={[0.1, 16, 16]} />}
        <meshStandardMaterial color={hovered ? 'white' : getColor()} />
      </mesh>
    </Interactive>
  );
}

export default function FBIGame() {
  const [collectedEvidence, setCollectedEvidence] = useState([]);
  const [analysisResult, setAnalysisResult] = useState('');
  const [blockchainStatus, setBlockchainStatus] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleCollect = async (type) => {
    if (collectedEvidence.includes(type)) return;

    setCollectedEvidence([...collectedEvidence, type]);
    setIsAnalyzing(true);
    setAnalysisResult(`Analyzing ${type}...`);

    // AI Analysis
    const result = await AIService.analyzeEvidence(type);
    setAnalysisResult(result);

    // Blockchain Log
    setBlockchainStatus(`Securing evidence ${type} on blockchain...`);
    const tx = await BlockchainService.logEvidence(type, { analysis: result });
    setBlockchainStatus(`Evidence secured! TX: ${tx.hash.substring(0, 10)}...`);
    setIsAnalyzing(false);
  };

  return (
    <div style={{ width: '100%', height: '80vh', position: 'relative', background: '#111' }}>
      <ARButton />
      <Canvas shadows camera={{ position: [0, 2, 5], fov: 50 }}>
        <XR>
          <Sky sunPosition={[100, 20, 100]} />
          <Environment preset="city" />
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} castShadow />

          <Controllers />
          <Hands />

          {/* Room / Floor */}
          <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
            <planeGeometry args={[10, 10]} />
            <meshStandardMaterial color="#333" />
          </mesh>

          <Evidence position={[-1, 1, -2]} type="gun" onCollect={handleCollect} />
          <Evidence position={[1, 1, -2]} type="laptop" onCollect={handleCollect} />
          <Evidence position={[0, 1, -3]} type="badge" onCollect={handleCollect} />

          <Text
            position={[0, 2.5, -4]}
            fontSize={0.3}
            color="white"
            anchorX="center"
            anchorY="middle"
          >
            FBI Crime Scene: Collect Evidence
          </Text>

          <OrbitControls />
          <ContactShadows opacity={0.4} scale={10} blur={2} far={4.5} />
        </XR>
      </Canvas>

      <div style={{
        position: 'absolute',
        bottom: 20,
        left: 20,
        right: 20,
        padding: '15px',
        background: 'rgba(0,0,0,0.8)',
        color: 'white',
        borderRadius: '8px',
        fontFamily: 'monospace',
        pointerEvents: 'none'
      }}>
        <div>Collected: {collectedEvidence.join(', ') || 'None'}</div>
        <div style={{ marginTop: '10px', color: '#00ff00' }}>{analysisResult}</div>
        <div style={{ marginTop: '5px', fontSize: '0.8em', color: '#888' }}>{blockchainStatus}</div>
      </div>
    </div>
  );
}
