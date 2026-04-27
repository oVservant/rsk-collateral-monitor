#!/usr/bin/env python3
"""Validate .env configuration before running."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
env_file = project_root / '.env'

def validate_env():
    """Validate environment configuration."""
    print("🔍 Validating .env configuration...")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Run: cp .env.example .env")
        return False
    
    load_dotenv(env_file)
    
    errors = []
    warnings = []
    
    # Required variables
    required = {
        'RSK_RPC_URL': 'RSK RPC endpoint',
        'TELEGRAM_BOT_TOKEN': 'Telegram bot token',
        'TELEGRAM_ADMIN_ID': 'Telegram admin ID',
    }
    
    for var, description in required.items():
        value = os.getenv(var)
        if not value:
            errors.append(f"Missing required variable: {var} ({description})")
        elif value == 'your_bot_token_here' or value == 'your_admin_id':
            errors.append(f"{var} still has placeholder value")
    
    # Contract addresses (should be verified)
    contracts = {
        'MOC_PLATFORM_ADDRESS': 'MoCPlatform contract',
        'MOC_HOLDER_ADDRESS': 'MoCHolder contract',
        'DOC_TOKEN_ADDRESS': 'DOC token contract',
    }
    
    for var, description in contracts.items():
        value = os.getenv(var)
        if not value:
            warnings.append(f"Missing contract address: {var} ({description})")
        elif value.startswith('0x') and len(value) != 42:
            errors.append(f"Invalid address format for {var}: {value[:10]}...")
        elif '5a5D5C5B5A5D5C5B' in value or '4854a59D4B2b' in value:
            warnings.append(f"{var} may still have placeholder value")
    
    # Thresholds
    try:
        warning = float(os.getenv('WARNING_THRESHOLD', '180'))
        critical = float(os.getenv('CRITICAL_THRESHOLD', '160'))
        liquidation = float(os.getenv('LIQUIDATION_THRESHOLD', '150'))
        
        if not (warning > critical > liquidation):
            errors.append("Thresholds must be: WARNING > CRITICAL > LIQUIDATION")
        
        if warning < 100 or warning > 500:
            warnings.append(f"Unusual WARNING_THRESHOLD: {warning}%")
            
    except ValueError as e:
        errors.append(f"Invalid threshold values: {e}")
    
    # Polling interval
    try:
        interval = int(os.getenv('POLL_INTERVAL_MINUTES', '10'))
        if interval < 1 or interval > 60:
            warnings.append(f"Unusual POLL_INTERVAL_MINUTES: {interval}")
    except ValueError:
        errors.append("POLL_INTERVAL_MINUTES must be a number")
    
    # Database path
    db_path = os.getenv('DATABASE_PATH', 'data/collateral_monitor.db')
    db_dir = Path(db_path).parent
    if not db_dir.exists():
        try:
            db_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created database directory: {db_dir}")
        except Exception as e:
            errors.append(f"Cannot create database directory: {e}")
    
    # Print results
    print("\n" + "="*60)
    
    if errors:
        print("❌ ERRORS (must fix before running):")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print("\n⚠️  WARNINGS (should review):")
        for warning in warnings:
            print(f"   • {warning}")
    
    if not errors and not warnings:
        print("✅ All validations passed!")
        print("\n🎉 Configuration is ready for production!")
        return True
    elif not errors:
        print("\n✅ No errors found. Warnings can be reviewed.")
        return True
    else:
        print("\n❌ Please fix errors before running.")
        return False

if __name__ == '__main__':
    success = validate_env()
    sys.exit(0 if success else 1)
