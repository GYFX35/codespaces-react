import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import App from './App';
import React from 'react';

test('renders Global Security Platform title', () => {
  render(<App />);
  const titleElements = screen.getAllByText(/Global Security Platform/i);
  expect(titleElements.length).toBeGreaterThan(0);
});

test('renders navigation buttons', () => {
  render(<App />);
  const marketplaceButtons = screen.getAllByText(/Marketplace/i);
  expect(marketplaceButtons.length).toBeGreaterThan(0);

  const scamButtons = screen.getAllByText(/Scam Analyzer/i);
  expect(scamButtons.length).toBeGreaterThan(0);

  const fakeNewsButtons = screen.getAllByText(/Fake News/i);
  expect(fakeNewsButtons.length).toBeGreaterThan(0);

  const fbiButtons = screen.getAllByText(/FBI Game/i);
  expect(fbiButtons.length).toBeGreaterThan(0);
});
