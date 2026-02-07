import { render, screen } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import FBIGame from './FBIGame';
import React from 'react';

// Mock Three.js and Canvas because they don't work well in JSDOM
vi.mock('@react-three/fiber', () => ({
  Canvas: ({ children }) => <div>{children}</div>,
  useFrame: () => {},
}));

vi.mock('@react-three/xr', () => ({
  XR: ({ children }) => <div>{children}</div>,
  ARButton: () => <button>AR Mode</button>,
  VRButton: () => <button>VR Mode</button>,
  Interactive: ({ children }) => <div>{children}</div>,
  Controllers: () => null,
  Hands: () => null,
}));

vi.mock('@react-three/drei', () => ({
  OrbitControls: () => null,
  Text: ({ children }) => <div>{children}</div>,
  Sky: () => null,
  ContactShadows: () => null,
  Environment: () => null,
}));

test('renders FBI Game component', () => {
  render(<FBIGame />);
  expect(screen.getByText(/FBI Crime Scene/i)).toBeDefined();
  expect(screen.getByText(/Collected: None/i)).toBeDefined();
});
