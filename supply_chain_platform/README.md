# Supply Chain & Logistics AI Platform

This platform provides a suite of tools for managing supply chain logistics, including a Digital Twin simulation, Incoterms navigator, and AI-driven logistics optimization.

## Features

1.  **Digital Twin (3D Simulation):**
    *   A real-time 3D representation of a warehouse environment.
    *   Visualizes Automated Guided Vehicles (AGVs) and cargo movement.
    *   Built with React Three Fiber and Three.js.
    *   Supports AR/VR modes.

2.  **Incoterms Navigator:**
    *   Comprehensive guide to Incoterms 2020 (EXW, FOB, CIF, DDP, etc.).
    *   Clarifies responsibilities and risks for buyers and sellers.

3.  **AI Logistics Engine:**
    *   **Delay Predictor:** Uses heuristics to predict shipment delays based on distance and weather conditions.
    *   **Inventory Risk Analysis:** Analyzes stock levels against demand forecasts to identify stockout risks.
    *   **Route Optimization:** Simulates optimal routing for logistics efficiency.

4.  **Blockchain Audit Trail:**
    *   Secures logistics events on a decentralized ledger using Ethers.js.
    *   Provides a transparent and immutable history of supply chain operations.

## Components

### CLI Tool (Python)
Located in `supply_chain_platform/supply_chain_main.py`.
Provides a command-line interface for:
- Incoterms lookup.
- AI Delay prediction.
- Inventory risk assessment.

**Usage:**
```bash
python3 supply_chain_platform/supply_chain_main.py
```

### Web Interface (React)
Integrated into the main application dashboard under the "Supply Chain" tab.
Includes:
- **Digital Twin View**: Interactive 3D warehouse.
- **Incoterms Navigator**: Interactive dropdown guide.
- **Logistics AI Dashboard**: Real-time AI analysis and Blockchain logging.

## File Structure
```
supply_chain_platform/
├── supply_chain_main.py      # Main CLI application
├── ai_logistics_engine.py    # Mock AI logic for logistics
├── incoterms_data.json       # Database of trade terms
└── README.md                 # This documentation
src/
└── SupplyChainPlatform.jsx   # React frontend component
```

## Future Enhancements
- Integration with real-time IoT sensors for live Digital Twin updates.
- Advanced NLP for automated Incoterm selection from contracts.
- Real blockchain integration with Ethereum/Polygon testnets.
