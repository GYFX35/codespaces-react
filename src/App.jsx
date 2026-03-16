import React, { useState } from 'react';
import './App.css';
import ScamAnalyzer from './ScamAnalyzer';
import FakeNewsAnalyzer from './FakeNewsAnalyzer';
import AIContentDetector from './AIContentDetector';
import FakeContentAnalyzer from './FakeContentAnalyzer';
import FBIGame from './FBIGame';
import SupplyChainPlatform from './SupplyChainPlatform';
import Marketplace from './Marketplace';

function App() {
  const [view, setView] = useState('marketplace');

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content" onClick={() => setView('marketplace')} style={{ cursor: 'pointer' }}>
          <h1>Global Security Platform</h1>
          <span className="official-badge">OFFICIAL</span>
        </div>
        <nav>
          <button className={view === 'marketplace' ? 'active' : ''} onClick={() => setView('marketplace')}>Marketplace</button>
          <button className={view === 'scam' ? 'active' : ''} onClick={() => setView('scam')}>Scam Analyzer</button>
          <button className={view === 'fake-news' ? 'active' : ''} onClick={() => setView('fake-news')}>Fake News</button>
          <button className={view === 'ai-content' ? 'active' : ''} onClick={() => setView('ai-content')}>AI Content</button>
          <button className={view === 'fake-content' ? 'active' : ''} onClick={() => setView('fake-content')}>Fake Content</button>
          <button className={view === 'fbi-game' ? 'active' : ''} onClick={() => setView('fbi-game')}>FBI Game</button>
          <button className={view === 'supply-chain' ? 'active' : ''} onClick={() => setView('supply-chain')}>Supply Chain</button>
        </nav>
      </header>
      <main>
        {view === 'marketplace' && <Marketplace setView={setView} />}
        {view === 'scam' && <ScamAnalyzer />}
        {view === 'fake-news' && <FakeNewsAnalyzer />}
        {view === 'ai-content' && <AIContentDetector />}
        {view === 'fake-content' && <FakeContentAnalyzer />}
        {view === 'fbi-game' && <FBIGame />}
        {view === 'supply-chain' && <SupplyChainPlatform />}
      </main>
      <footer className="global-footer">
        <p>© 2024 Global Security Platform | Official Domain: <a href="https://global-security-platform.com">global-security-platform.com</a></p>
      </footer>
    </div>
  );
}

export default App;
