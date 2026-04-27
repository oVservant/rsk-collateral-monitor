"""Database models and repository for BTC Collateral Monitor."""
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import json

from config.settings import settings

logger = logging.getLogger('collateral_monitor.db')


class Database:
    """SQLite database wrapper."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialize database and create tables."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Read and execute schema
        schema_file = Path(__file__).parent / 'schema.sql'
        if schema_file.exists():
            with open(schema_file, 'r') as f:
                schema = f.read()
                cursor.executescript(schema)
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized: {self.db_path}")
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # User operations
    def add_user(self, telegram_id: str, username: str = None, wallet: str = None) -> int:
        """Add or update user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (telegram_id, telegram_username, wallet_address)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                telegram_username = excluded.telegram_username,
                wallet_address = excluded.wallet_address,
                is_active = 1
        """, (telegram_id, username, wallet))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"User added/updated: {telegram_id}")
        return user_id
    
    def get_user(self, telegram_id: str) -> Optional[Dict]:
        """Get user by Telegram ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # Position operations
    def add_position(self, position_id: str, wallet_address: str, protocol: str = 'MoneyOnChain') -> int:
        """Add or update position."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO positions (position_id, wallet_address, protocol)
            VALUES (?, ?, ?)
            ON CONFLICT(position_id, wallet_address) DO UPDATE SET
                last_updated = CURRENT_TIMESTAMP,
                is_active = 1
        """, (position_id, wallet_address, protocol))
        
        pos_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Position added/updated: {position_id}")
        return pos_id
    
    def get_active_positions(self) -> List[Dict]:
        """Get all active positions."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM positions WHERE is_active = 1
        """)
        
        positions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return positions
    
    # Snapshot operations
    def add_snapshot(self, position_id: str, wallet_address: str, 
                     collateral: str, debt: str, ratio: float,
                     rbtc_price: float, doc_price: float) -> int:
        """Add position snapshot."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO position_snapshots 
            (position_id, wallet_address, collateral_amount, debt_amount, 
             collateral_ratio, rbtc_price_usd, doc_price_usd)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (position_id, wallet_address, collateral, debt, ratio, rbtc_price, doc_price))
        
        snapshot_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return snapshot_id
    
    def get_position_history(self, position_id: str, limit: int = 100) -> List[Dict]:
        """Get historical snapshots for a position."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM position_snapshots 
            WHERE position_id = ?
            ORDER BY snapshot_timestamp DESC
            LIMIT ?
        """, (position_id, limit))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return history
    
    # Alert operations
    def add_alert(self, position_id: str, wallet_address: str, 
                  alert_type: str, ratio: float, threshold: float) -> int:
        """Add alert record."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO alerts 
            (position_id, wallet_address, alert_type, collateral_ratio, threshold_breached)
            VALUES (?, ?, ?, ?, ?)
        """, (position_id, wallet_address, alert_type, ratio, threshold))
        
        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Alert recorded: {alert_type} for position {position_id}")
        return alert_id
    
    def update_alert_sent(self, alert_id: int, message_id: str):
        """Mark alert as sent via Telegram."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE alerts SET telegram_sent = 1, telegram_message_id = ?
            WHERE id = ?
        """, (message_id, alert_id))
        
        conn.commit()
        conn.close()
    
    def get_unsent_alerts(self) -> List[Dict]:
        """Get alerts that haven't been sent yet."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM alerts WHERE telegram_sent = 0
            ORDER BY created_at ASC
        """)
        
        alerts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return alerts
    
    # Metrics operations
    def record_metric(self, metric_name: str, metric_value: str):
        """Record system metric."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO system_metrics (metric_name, metric_value)
            VALUES (?, ?)
        """, (metric_name, metric_value))
        
        conn.commit()
        conn.close()


# Singleton instance
_db = None

def get_database() -> Database:
    """Get or create Database singleton."""
    global _db
    if _db is None:
        _db = Database()
    return _db
