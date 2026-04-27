#!/usr/bin/env python3
"""
BTC Collateral Monitor - Position Polling Script

Run this script via cron every 5-10 minutes to:
1. Fetch positions from RSK blockchain
2. Calculate collateral ratios
3. Store snapshots in database
4. Send Telegram alerts for threshold breaches

Usage:
    python poll_positions.py

Cron example (every 10 minutes):
    */10 * * * * cd /home/ovservant/projects/rsk-collateral-monitor && python scripts/poll_positions.py
"""
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from config.logging_config import setup_logging
from core.contract_reader import get_contract_reader
from core.ratio_calculator import get_ratio_calculator
from db.models import get_database
from bot.telegram_bot import get_bot

# Initialize logging
log_file = project_root / 'data' / 'poller.log'
logger = setup_logging(str(log_file))


def poll_positions():
    """Main polling function."""
    logger.info("=" * 60)
    logger.info(f"Starting poll at {datetime.now().isoformat()}")
    
    try:
        # Initialize components
        contract_reader = get_contract_reader()
        ratio_calculator = get_ratio_calculator()
        db = get_database()
        bot = get_bot()
        
        # Check connection
        if not contract_reader.is_connected():
            logger.error("Failed to connect to RSK node")
            return False
        
        logger.info(f"Connected to RSK node (block {contract_reader.get_block_number()})")
        
        # Get all active positions from database
        positions = db.get_active_positions()
        logger.info(f"Found {len(positions)} active positions to monitor")
        
        if not positions:
            logger.info("No positions to monitor. Users can register via Telegram bot.")
            return True
        
        # Process each position
        alerts_triggered = 0
        
        for position in positions:
            try:
                # Fetch latest position data from blockchain
                wallet = position['wallet_address']
                position_id = position['position_id']
                
                # Get position data from contract
                position_data = contract_reader.get_position(int(position_id))
                
                if not position_data:
                    logger.warning(f"Position {position_id} not found on-chain")
                    continue
                
                # Calculate ratio and check thresholds
                processed = ratio_calculator.process_position(position_data)
                
                logger.info(
                    f"Position {position_id}: "
                    f"Ratio={processed['collateral_ratio']:.2f}% "
                    f"Status={processed['alert_level']}"
                )
                
                # Store snapshot
                db.add_snapshot(
                    position_id=position_id,
                    wallet_address=wallet,
                    collateral=str(position_data['collateral_wei']),
                    debt=str(position_data['debt_wei']),
                    ratio=processed['collateral_ratio'],
                    rbtc_price=processed['rbtc_price_usd'],
                    doc_price=processed['doc_price_usd']
                )
                
                # Send alerts if needed
                if processed['is_warning'] or processed['is_critical']:
                    alert_type = 'CRITICAL' if processed['is_critical'] else 'WARNING'
                    
                    # Record alert in database
                    alert_id = db.add_alert(
                        position_id=position_id,
                        wallet_address=wallet,
                        alert_type=alert_type,
                        ratio=processed['collateral_ratio'],
                        threshold=settings.CRITICAL_THRESHOLD if processed['is_critical'] else settings.WARNING_THRESHOLD
                    )
                    
                    # Get user for this wallet
                    # In production, query users by wallet_address
                    # For now, send to admin
                    if bot and settings.TELEGRAM_ADMIN_ID:
                        bot.send_alert(
                            telegram_id=settings.TELEGRAM_ADMIN_ID,
                            position_data=processed,
                            ratio=processed['collateral_ratio'],
                            alert_type=alert_type
                        )
                        db.update_alert_sent(alert_id, "sent")
                    
                    alerts_triggered += 1
                
            except Exception as e:
                logger.error(f"Error processing position {position.get('position_id')}: {e}")
                continue
        
        # Record metrics
        db.record_metric('positions_monitored', str(len(positions)))
        db.record_metric('alerts_triggered', str(alerts_triggered))
        
        logger.info(f"Poll completed: {len(positions)} positions, {alerts_triggered} alerts")
        return True
        
    except Exception as e:
        logger.error(f"Poll failed with error: {e}", exc_info=True)
        return False
    
    finally:
        logger.info(f"Poll finished at {datetime.now().isoformat()}")
        logger.info("=" * 60)


if __name__ == '__main__':
    success = poll_positions()
    sys.exit(0 if success else 1)
