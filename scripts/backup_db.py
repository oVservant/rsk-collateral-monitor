#!/usr/bin/env python3
"""Backup database with rotation."""
import sys
import os
from pathlib import Path
import shutil
from datetime import datetime
import gzip

project_root = Path(__file__).parent.parent
db_path = project_root / 'data' / 'collateral_monitor.db'
backup_dir = project_root / 'backups'

def backup_database(keep_days: int = 7):
    """Backup database and rotate old backups."""
    print("💾 Backing up database...")
    
    if not db_path.exists():
        print("❌ Database not found")
        return False
    
    # Create backup directory
    backup_dir.mkdir(exist_ok=True)
    
    # Generate backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'collateral_monitor_{timestamp}.db'
    compressed_file = backup_dir / f'collateral_monitor_{timestamp}.db.gz'
    
    try:
        # Copy database
        shutil.copy2(db_path, backup_file)
        print(f"✅ Backup created: {backup_file.name}")
        
        # Compress backup
        with open(backup_file, 'rb') as f_in:
            with gzip.open(compressed_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove uncompressed backup
        backup_file.unlink()
        print(f"✅ Compressed: {compressed_file.name}")
        
        # Rotate old backups
        print("\n🔄 Rotating old backups...")
        cutoff = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        rotated = 0
        
        for backup in backup_dir.glob('collateral_monitor_*.db.gz'):
            if backup.stat().st_mtime < cutoff:
                backup.unlink()
                print(f"   Deleted: {backup.name}")
                rotated += 1
        
        if rotated == 0:
            print("   No old backups to rotate")
        
        # Show backup stats
        backups = list(backup_dir.glob('collateral_monitor_*.db.gz'))
        total_size = sum(b.stat().st_size for b in backups)
        
        print(f"\n📊 Backup Summary:")
        print(f"   Total backups: {len(backups)}")
        print(f"   Total size: {total_size / 1024:.2f} KB")
        print(f"   Kept: {keep_days} days")
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

if __name__ == '__main__':
    keep_days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    success = backup_database(keep_days)
    sys.exit(0 if success else 1)
