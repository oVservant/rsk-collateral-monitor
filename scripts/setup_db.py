#!/usr/bin/env python3
"""Initialize the database for BTC Collateral Monitor."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from db.models import Database
from config.logging_config import setup_logging

logger = setup_logging()

def main():
    """Initialize database."""
    print("🔧 Initializing database...")
    
    try:
        db = Database()
        print(f"✅ Database created at: {db.db_path}")
        
        # Verify tables
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        print(f"✅ Tables created: {', '.join(tables)}")
        print("\n✅ Database setup complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
