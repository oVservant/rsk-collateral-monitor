#!/bin/bash
# BTC Collateral Monitor - Cron Job Installation Script

set -e

PROJECT_DIR="/home/ovservant/projects/rsk-collateral-monitor"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON="$VENV_DIR/bin/python"
POLL_SCRIPT="$PROJECT_DIR/scripts/poll_positions.py"
LOG_FILE="$PROJECT_DIR/data/cron.log"

echo "🔧 Installing BTC Collateral Monitor cron job..."

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found at $VENV_DIR"
    echo "Run: cd $PROJECT_DIR && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if .env exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "⚠️  .env file not found. Copy from .env.example and configure first."
    echo "Run: cp $PROJECT_DIR/.env.example $PROJECT_DIR/.env && nano $PROJECT_DIR/.env"
    exit 1
fi

# Create log directory
mkdir -p "$PROJECT_DIR/data"

# Backup existing crontab
crontab -l > "$PROJECT_DIR/data/crontab.backup.$(date +%Y%m%d%H%M%S)" 2>/dev/null || true

# Add cron job
CRON_JOB="*/10 * * * * cd $PROJECT_DIR && $PYTHON $POLL_SCRIPT >> $LOG_FILE 2>&1"

# Check if job already exists
if crontab -l 2>/dev/null | grep -q "$POLL_SCRIPT"; then
    echo "⚠️  Cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "$POLL_SCRIPT" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null | grep -v "^$"; echo "$CRON_JOB") | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "📋 Cron job details:"
echo "   Schedule: Every 10 minutes"
echo "   Log file: $LOG_FILE"
echo ""
echo "📝 Verify with: crontab -l"
echo "📊 View logs with: tail -f $LOG_FILE"
echo ""
echo "🔧 To remove: crontab -e  # Delete the line with poll_positions.py"
