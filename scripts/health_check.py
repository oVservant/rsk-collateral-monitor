#!/usr/bin/env python3
"""Health check script for monitoring."""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3

project_root = Path(__file__).parent.parent
db_path = project_root / 'data' / 'collateral_monitor.db'
log_file = project_root / 'data' / 'poller.log'

def check_database():
    """Check database health."""
    print("🗄️  Checking database...")
    
    if not db_path.exists():
        print("   ❌ Database not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check integrity
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()[0]
        if result != 'ok':
            print(f"   ❌ Database integrity check failed: {result}")
            conn.close()
            return False
        
        # Check table existence
        tables = ['users', 'positions', 'position_snapshots', 'alerts']
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            if table not in existing_tables:
                print(f"   ❌ Missing table: {table}")
                conn.close()
                return False
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM positions")
        pos_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM position_snapshots")
        snapshot_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"   ✅ Database OK ({pos_count} positions, {snapshot_count} snapshots)")
        return True
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def check_last_poll():
    """Check if polling is running."""
    print("\n⏰ Checking last poll...")
    
    if not log_file.exists():
        print("   ⚠️  No poller log found (first run?)")
        return True
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        # Find last successful poll
        last_poll_time = None
        for line in reversed(lines[-100:]):  # Check last 100 lines
            if 'Poll completed' in line:
                # Extract timestamp from log line
                try:
                    timestamp_str = line.split(' - ')[0]
                    last_poll_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    break
                except:
                    pass
        
        if not last_poll_time:
            print("   ⚠️  No completed poll found in logs")
            return True
        
        # Check if poll is recent (within last 20 minutes)
        now = datetime.now()
        diff = now - last_poll_time
        
        if diff > timedelta(minutes=20):
            print(f"   ⚠️  Last poll was {diff.seconds // 60} minutes ago")
            return False
        else:
            print(f"   ✅ Last poll {diff.seconds // 60} minutes ago")
            return True
            
    except Exception as e:
        print(f"   ❌ Error reading logs: {e}")
        return False

def check_rsk_connection():
    """Check RSK node connection."""
    print("\n🔗 Checking RSK connection...")
    
    try:
        from core.contract_reader import get_contract_reader
        reader = get_contract_reader()
        
        if not reader.is_connected():
            print("   ❌ Cannot connect to RSK node")
            return False
        
        block_number = reader.get_block_number()
        print(f"   ✅ Connected to RSK (Block #{block_number})")
        return True
        
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return False

def check_disk_space():
    """Check available disk space."""
    print("\n💾 Checking disk space...")
    
    try:
        import shutil
        total, used, free = shutil.disk_usage(project_root)
        free_gb = free / (1024**3)
        
        if free_gb < 1:
            print(f"   ⚠️  Low disk space: {free_gb:.2f} GB free")
            return False
        else:
            print(f"   ✅ {free_gb:.2f} GB free")
            return True
            
    except Exception as e:
        print(f"   ❌ Error checking disk space: {e}")
        return True  # Don't fail on this

def main():
    """Run all health checks."""
    print("="*60)
    print("BTC Collateral Monitor - Health Check")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*60)
    
    checks = [
        check_database,
        check_last_poll,
        check_rsk_connection,
        check_disk_space,
    ]
    
    results = []
    for check in checks:
        try:
            results.append(check())
        except Exception as e:
            print(f"\n❌ Check {check.__name__} failed with error: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All checks passed ({passed}/{total})")
        print("\n🎉 System is healthy!")
        return 0
    else:
        print(f"⚠️  Some checks failed ({passed}/{total} passed)")
        print("\n❌ Please review errors above")
        return 1

if __name__ == '__main__':
    sys.exit(main())
