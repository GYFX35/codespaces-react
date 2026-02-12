import React, { useState } from 'react';
import './App.css';
import ScamAnalyzer from './ScamAnalyzer';
import FakeNewsAnalyzer from './FakeNewsAnalyzer';
import FBIGame from './FBIGame';
import SupplyChainPlatform from './SupplyChainPlatform';

function App() {
  const [view, setView] = useState('scam');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Universal Security Analyzer</h1>
        <nav>
          <button className={view === 'scam' ? 'active' : ''} onClick={() => setView('scam')}>Scam Analyzer</button>
          <button className={view === 'fake-news' ? 'active' : ''} onClick={() => setView('fake-news')}>Fake News Analyzer</button>
          <button className={view === 'fbi-game' ? 'active' : ''} onClick={() => setView('fbi-game')}>FBI AR Game</button>
          <button className={view === 'supply-chain' ? 'active' : ''} onClick={() => setView('supply-chain')}>Supply Chain</button>
        </nav>
      </header>
      <main>
        {view === 'scam' && <ScamAnalyzer />}
        {view === 'fake-news' && <FakeNewsAnalyzer />}
        {view === 'fbi-game' && <FBIGame />}
        {view === 'supply-chain' && <SupplyChainPlatform />}
      </main>
    </div>
  );
}

export default App;
