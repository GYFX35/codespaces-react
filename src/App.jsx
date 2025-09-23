import React, { useState } from 'react';
import './App.css';
import ScamAnalyzer from './ScamAnalyzer';
import FakeNewsAnalyzer from './FakeNewsAnalyzer';

function App() {
  const [view, setView] = useState('scam');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Universal Security Analyzer</h1>
        <nav>
          <button onClick={() => setView('scam')}>Scam Analyzer</button>
          <button onClick={() => setView('fake-news')}>Fake News Analyzer</button>
        </nav>
      </header>
      <main>
        {view === 'scam' && <ScamAnalyzer />}
        {view === 'fake-news' && <FakeNewsAnalyzer />}
      </main>
    </div>
  );
}

export default App;
