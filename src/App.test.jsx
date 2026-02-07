import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import App from './App';
import React from 'react';

test('renders Universal Security Analyzer title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Universal Security Analyzer/i);
  expect(titleElement).toBeDefined();
});

test('renders navigation buttons', () => {
  render(<App />);
  const scamButtons = screen.getAllByText(/Scam Analyzer/i);
  expect(scamButtons.length).toBeGreaterThan(0);

  const fakeNewsButtons = screen.getAllByText(/Fake News Analyzer/i);
  expect(fakeNewsButtons.length).toBeGreaterThan(0);

  const fbiButtons = screen.getAllByText(/FBI AR Game/i);
  expect(fbiButtons.length).toBeGreaterThan(0);
});
