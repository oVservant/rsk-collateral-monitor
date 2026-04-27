#!/usr/bin/env python3
"""
Migration script from SQLite to PostgreSQL.

Usage:
    python scripts/migrate_to_postgres.py

Prerequisites:
    - PostgreSQL installed and running
    - Database created: CREATE DATABASE collateral_monitor;
    - Update .env with DATABASE_URL=postgresql://user:pass@localhost/collateral_monitor
"""
import sys
import os
from pathlib import Path
import sqlite3
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv(project_root / '.env')

# PostgreSQL schema
POSTGRES_SCHEMA = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id TEXT UNIQUE NOT NULL,
    telegram_username TEXT,
    wallet_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    notification_preferences JSONB DEFAULT '{"warning": true, "critical": true}'
);

-- Monitored positions table
CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    protocol TEXT DEFAULT 'MoneyOnChain',
    contract_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    UNIQUE(position_id, wallet_address)
);

-- Collateral ratio snapshots
CREATE TABLE IF NOT EXISTS position_snapshots (
    id SERIAL PRIMARY KEY,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    collateral_amount TEXT,
    debt_amount TEXT,
    collateral_ratio DECIMAL(10,4),
    rbtc_price_usd DECIMAL(20,8),
    doc_price_usd DECIMAL(20,8),
    snapshot_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alert history
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    position_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    collateral_ratio DECIMAL(10,4),
    threshold_breached DECIMAL(10,4),
    telegram_sent BOOLEAN DEFAULT false,
    telegram_message_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT false
);

-- System metrics
CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name TEXT NOT NULL,
    metric_value TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_telegram ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_wallet ON users(wallet_address);
CREATE INDEX IF NOT EXISTS idx_snapshots_position ON position_snapshots(position_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_timestamp ON position_snapshots(snapshot_timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_position ON alerts(position_id);
CREATE INDEX IF NOT EXISTS idx_positions_wallet ON positions(wallet_address);
"""

def migrate_sqlite_to_postgres():
    """Migrate data from SQLite to PostgreSQL."""
    print("🔄 Starting migration from SQLite to PostgreSQL...")
    
    # Get paths
    sqlite_db = project_root / 'data' / 'collateral_monitor.db'
    
    if not sqlite_db.exists():
        print("❌ SQLite database not found. Run setup first.")
        return False
    
    # Connect to SQLite
    print("\n📊 Connecting to SQLite...")
    sqlite_conn = sqlite3.connect(sqlite_db)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to PostgreSQL
    print("📊 Connecting to PostgreSQL...")
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found in .env")
        print("   Add: DATABASE_URL=postgresql://user:pass@localhost/collateral_monitor")
        sqlite_conn.close()
        return False
    
    try:
        pg_conn = psycopg2.connect(db_url)
        pg_cursor = pg_conn.cursor()
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        sqlite_conn.close()
        return False
    
    # Create PostgreSQL schema
    print("\n🏗️  Creating PostgreSQL schema...")
    try:
        pg_cursor.execute(POSTGRES_SCHEMA)
        pg_conn.commit()
        print("✅ Schema created successfully")
    except Exception as e:
        print(f"❌ Failed to create schema: {e}")
        pg_conn.rollback()
        sqlite_conn.close()
        pg_conn.close()
        return False
    
    # Migrate users
    print("\n👥 Migrating users...")
    try:
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        if users:
            insert_query = """
                INSERT INTO users (telegram_id, telegram_username, wallet_address, created_at, is_active, notification_preferences)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (telegram_id) DO NOTHING
            """
            execute_batch(pg_cursor, insert_query, users, page_size=100)
            pg_conn.commit()
            print(f"✅ Migrated {len(users)} users")
        else:
            print("   No users to migrate")
    except Exception as e:
        print(f"❌ Failed to migrate users: {e}")
        pg_conn.rollback()
    
    # Migrate positions
    print("\n📍 Migrating positions...")
    try:
        sqlite_cursor.execute("SELECT * FROM positions")
        positions = sqlite_cursor.fetchall()
        
        if positions:
            insert_query = """
                INSERT INTO positions (position_id, wallet_address, protocol, contract_address, created_at, last_updated, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (position_id, wallet_address) DO NOTHING
            """
            execute_batch(pg_cursor, insert_query, positions, page_size=100)
            pg_conn.commit()
            print(f"✅ Migrated {len(positions)} positions")
        else:
            print("   No positions to migrate")
    except Exception as e:
        print(f"❌ Failed to migrate positions: {e}")
        pg_conn.rollback()
    
    # Migrate snapshots
    print("\n📸 Migrating snapshots...")
    try:
        sqlite_cursor.execute("SELECT * FROM position_snapshots")
        snapshots = sqlite_cursor.fetchall()
        
        if snapshots:
            insert_query = """
                INSERT INTO position_snapshots (position_id, wallet_address, collateral_amount, debt_amount, collateral_ratio, rbtc_price_usd, doc_price_usd, snapshot_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            execute_batch(pg_cursor, insert_query, snapshots, page_size=100)
            pg_conn.commit()
            print(f"✅ Migrated {len(snapshots)} snapshots")
        else:
            print("   No snapshots to migrate")
    except Exception as e:
        print(f"❌ Failed to migrate snapshots: {e}")
        pg_conn.rollback()
    
    # Migrate alerts
    print("\n🚨 Migrating alerts...")
    try:
        sqlite_cursor.execute("SELECT * FROM alerts")
        alerts = sqlite_cursor.fetchall()
        
        if alerts:
            insert_query = """
                INSERT INTO alerts (position_id, wallet_address, alert_type, collateral_ratio, threshold_breached, telegram_sent, telegram_message_id, created_at, acknowledged)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            execute_batch(pg_cursor, insert_query, alerts, page_size=100)
            pg_conn.commit()
            print(f"✅ Migrated {len(alerts)} alerts")
        else:
            print("   No alerts to migrate")
    except Exception as e:
        print(f"❌ Failed to migrate alerts: {e}")
        pg_conn.rollback()
    
    # Close connections
    sqlite_conn.close()
    pg_conn.close()
    
    print("\n" + "="*60)
    print("✅ Migration completed successfully!")
    print("\n📝 Next steps:")
    print("   1. Update .env: DATABASE_URL=postgresql://...")
    print("   2. Test connection: python scripts/health_check.py")
    print("   3. Backup old SQLite database")
    print("   4. Deploy with PostgreSQL")
    
    return True

if __name__ == '__main__':
    success = migrate_sqlite_to_postgres()
    sys.exit(0 if success else 1)
