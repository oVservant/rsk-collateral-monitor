-- BTC Collateral Monitor Database Schema

-- Users table (Telegram users subscribed to alerts)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE NOT NULL,
    telegram_username TEXT,
    wallet_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    notification_preferences TEXT DEFAULT '{"warning": true, "critical": true}'
);

-- Monitored positions table
CREATE TABLE IF NOT EXISTS positions (
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
CREATE TABLE IF NOT EXISTS position_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    collateral_amount TEXT,
    debt_amount TEXT,
    collateral_ratio DECIMAL(10,4),
    rbtc_price_usd DECIMAL(20,8),
    doc_price_usd DECIMAL(20,8),
    snapshot_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
);

-- Alert history
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    collateral_ratio DECIMAL(10,4),
    threshold_breached DECIMAL(10,4),
    telegram_sent BOOLEAN DEFAULT 0,
    telegram_message_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT 0
);

-- System metrics
CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_snapshots_position ON position_snapshots(position_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_timestamp ON position_snapshots(snapshot_timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_position ON alerts(position_id);
CREATE INDEX IF NOT EXISTS idx_positions_wallet ON positions(wallet_address);
