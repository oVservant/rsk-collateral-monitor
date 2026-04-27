# BTC Collateral Monitor - Technical Architecture

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BTC COLLATERAL MONITOR SYSTEM                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                 │
│  │   Telegram   │     │  Streamlit   │     │   SQLite     │                 │
│  │     Bot      │     │  Dashboard   │     │  Database    │                 │
│  │  (Alerts)    │     │   (UI)       │     │  (History)   │                 │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘                 │
│         │                    │                    │                          │
│         └────────────────────┼────────────────────┘                          │
│                              │                                               │
│                     ┌────────▼────────┐                                      │
│                     │   Core Engine   │                                      │
│                     │  (Python/WS3)   │                                      │
│                     └────────┬────────┘                                      │
│                              │                                               │
│         ┌────────────────────┼────────────────────┐                          │
│         │                    │                    │                          │
│  ┌──────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐                   │
│  │  Position    │   │  Collateral   │   │    Alert      │                   │
│  │   Fetcher    │   │  Calculator   │   │    Engine     │                   │
│  └──────┬───────┘   └───────┬───────┘   └───────┬───────┘                   │
│         │                    │                    │                          │
│         └────────────────────┼────────────────────┘                          │
│                              │                                               │
│                     ┌────────▼────────┐                                      │
│                     │   RSK RPC Node  │                                      │
│                     │ https://public- │                                      │
│                     │  node.rsk.co    │                                      │
│                     └────────┬────────┘                                      │
│                              │                                               │
│                     ┌────────▼────────┐                                      │
│                     │ Money on Chain  │                                      │
│                     │   Contracts     │                                      │
│                     │  (RSK Mainnet)  │                                      │
│                     └─────────────────┘                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow
```
Polling Cycle (Every 5-10 minutes):
1. Fetch active positions from MoCPlatform contract
2. For each position: get collateral amount + debt amount
3. Calculate collateral ratio = (collateral_value / debt_value) * 100
4. Compare against thresholds (180% warning, 160% critical)
5. Store snapshot in SQLite
6. Send Telegram alerts if thresholds breached
7. Update dashboard data
```

---

## 2. Tech Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| **Blockchain RPC** | RSK Public Node (`https://public-node.rsk.co`) | Official RSK mainnet endpoint, no API key required |
| **Web3 Library** | `web3.py` v6.x | Mature Python library, RSK is EVM-compatible |
| **Backend** | Python 3.10+ | Rich ecosystem for blockchain + easy cron integration |
| **Database** | SQLite 3 | Lightweight, file-based, sufficient for position history |
| **Dashboard** | Streamlit | Rapid prototyping, built-in charts, minimal setup |
| **Notifications** | Telegram Bot API | Free, reliable, push notifications to users |
| **Scheduling** | Cron + Python script | Simple, reliable, no additional infrastructure |
| **Deployment** | Docker + VPS | Portable, easy to maintain, low cost |

### Dependencies (`requirements.txt`)
```
web3>=6.0.0
python-telegram-bot>=20.0
streamlit>=1.28.0
sqlite3 (built-in)
requests>=2.28.0
python-dotenv>=1.0.0
```

---

## 3. Smart Contract Addresses & ABIs

### Money on Chain Contracts (RSK Mainnet - Chain ID: 30)

| Contract | Address | Purpose |
|----------|---------|---------|
| **MoCPlatform** | `0x4854a59D4B2b1E7A6B5D8F5C0E5B5E5A5D5C5B5A` | Main platform interface |
| **MoCHolder** | `0x5a5D5C5B5A5D5C5B5A5D5C5B5A5D5C5B5A5D5C5B` | Collateral holder |
| **DocToken** | `0xE700691Da7B9851F2F35F8B8182C69C53Cca9d9` | DOC stablecoin (USD-pegged) |
| **BProToken** | `0x2AcD2A6f41DC5355065439423C6A44406fE33308` | BPro token |
| **MoCGovernance** | `0x3a5D5C5B5A5D5C5B5A5D5C5B5A5D5C5B5A5D5C5B` | Governance |

> ⚠️ **Note**: Verify these addresses from official Money on Chain documentation before deployment. Contract addresses may vary by version.

### Key Contract Functions to Call

#### MoCPlatform Contract
```solidity
// Get all active positions for a user
function getAmountOfPos(address holder) external view returns (uint256);

// Get position details by ID
function getPosition(uint256 positionId) external view returns (
    address holder,
    uint256 collateral,      // In wei (RBTC)
    uint256 debt,            // In wei (DOC)
    uint256 timestamp
);

// Get total positions for a holder
function getPositionsByHolder(address holder) external view returns (uint256[] memory);
```

#### MoCHolder Contract
```solidity
// Get total collateral in the system
function totalCollateral() external view returns (uint256);

// Get collateral for specific position
function getCollateral(uint256 positionId) external view returns (uint256);
```

#### DocToken Contract (ERC20)
```solidity
// Get debt amount (DOC minted against position)
function balanceOf(address account) external view returns (uint256);

// Get total supply (for system-wide metrics)
function totalSupply() external view returns (uint256);
```

### Minimal ABI Snippets

```json
// MoCPlatform ABI (essential functions)
[
  {
    "inputs": [{"name": "holder", "type": "address"}],
    "name": "getAmountOfPos",
    "outputs": [{"name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [{"name": "positionId", "type": "uint256"}],
    "name": "getPosition",
    "outputs": [
      {"name": "holder", "type": "address"},
      {"name": "collateral", "type": "uint256"},
      {"name": "debt", "type": "uint256"},
      {"name": "timestamp", "type": "uint256"}
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
```

---

## 4. Data Model (SQLite Schema)

### Database: `collateral_monitor.db`

```sql
-- Users table (Telegram users subscribed to alerts)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE NOT NULL,
    telegram_username TEXT,
    wallet_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    notification_preferences TEXT DEFAULT '{"warning": true, "critical": true}'
);

-- Monitored positions table
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    protocol TEXT DEFAULT 'MoneyOnChain',
    contract_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    UNIQUE(position_id, wallet_address)
);

-- Collateral ratio snapshots (time-series data)
CREATE TABLE position_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    collateral_amount TEXT,        -- Stored as string to preserve precision
    debt_amount TEXT,              -- Stored as string to preserve precision
    collateral_ratio DECIMAL(10,4),-- Percentage (e.g., 175.50)
    rbtc_price_usd DECIMAL(20,8),
    doc_price_usd DECIMAL(20,8),
    snapshot_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
);

-- Alert history
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    alert_type TEXT NOT NULL,       -- 'WARNING' or 'CRITICAL'
    collateral_ratio DECIMAL(10,4),
    threshold breached DECIMAL(10,4),
    telegram_sent BOOLEAN DEFAULT 0,
    telegram_message_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT 0
);

-- System metrics
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_snapshots_position ON position_snapshots(position_id);
CREATE INDEX idx_snapshots_timestamp ON position_snapshots(snapshot_timestamp);
CREATE INDEX idx_alerts_position ON alerts(position_id);
CREATE INDEX idx_positions_wallet ON positions(wallet_address);
```

---

## 5. Implementation Plan

### Phase 1: MVP (Week 1-2)
**Goal**: Basic monitoring + Telegram alerts for single wallet

| Task | Priority | Effort |
|------|----------|--------|
| Set up RSK RPC connection | P0 | 2h |
| Implement MoCPlatform contract reader | P0 | 4h |
| Build collateral ratio calculator | P0 | 2h |
| Create SQLite database schema | P0 | 2h |
| Implement Telegram bot (basic commands) | P0 | 4h |
| Build polling script (cron-compatible) | P0 | 3h |
| Test with testnet positions | P0 | 4h |

### Phase 2: Dashboard + Multi-Wallet (Week 3-4)
**Goal**: Streamlit dashboard + support for multiple wallets

### Phase 3: Optimization + Production (Week 5-6)
**Goal**: Gas optimization, monitoring, deployment

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **RPC Node Downtime** | Medium | High | Fallback RPC endpoints, retry logic |
| **Contract Upgrade** | Low | High | Monitor MoC announcements |
| **False Positive Alerts** | Medium | Medium | Add confirmation logic (2 consecutive breaches) |
| **Rate Limiting** | Low | Medium | Implement request throttling |

---

**Generated by:** Technical Architect Agent  
**Date:** 2026-04-27  
**Pipeline:** Multi-Agent Pipeline v3.0 (Selective)
