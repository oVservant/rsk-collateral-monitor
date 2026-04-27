# ₿ BTC Collateral Monitor

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue)](https://github.com/oVservant/rsk-collateral-monitor)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Monitor BTC-backed positions on Rootstock's Money on Chain protocol and receive Telegram alerts when collateral ratios approach liquidation levels.

**🔗 Repository:** https://github.com/oVservant/rsk-collateral-monitor

## Features

- 🔍 **Real-time Monitoring**: Track collateral ratios for multiple wallets
- 📊 **Telegram Alerts**: Get notified when positions approach liquidation
- 📈 **Dashboard**: Streamlit web UI for visualizing positions and history
- ⏰ **Automated**: Cron job polling every 5-10 minutes
- 💾 **Historical Data**: SQLite database for trend analysis

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Telegram   │     │  Streamlit   │     │   SQLite     │
│     Bot      │     │  Dashboard   │     │  Database    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       └────────────────────┼────────────────────┘
                            │
                   ┌────────▼────────┐
                   │   Core Engine   │
                   │  (Python/WS3)   │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │   RSK RPC Node  │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ Money on Chain  │
                   │   Contracts     │
                   └─────────────────┘
```

## Quick Start

### 1. Clone and Install

```bash
cd /home/ovservant/projects/rsk-collateral-monitor
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
nano .env  # Edit with your settings
```

Required settings:
- `TELEGRAM_BOT_TOKEN`: Get from @BotFather on Telegram
- `MOC_PLATFORM_ADDRESS`: Money on Chain contract address (verify!)

### 3. Initialize Database

```bash
python scripts/setup_db.py
```

### 4. Test Connection

```bash
python -c "from core.contract_reader import get_contract_reader; print(get_contract_reader().is_connected())"
```

### 5. Run Polling Script (Manual Test)

```bash
python scripts/poll_positions.py
```

### 6. Set Up Cron Job

```bash
crontab -e

# Add this line (poll every 10 minutes):
*/10 * * * * cd /home/ovservant/projects/rsk-collateral-monitor && python scripts/poll_positions.py >> data/cron.log 2>&1
```

### 7. Start Dashboard

```bash
streamlit run dashboard/app.py
```

Access at: `http://localhost:8501`

## Usage

### Telegram Bot Commands

- `/start` - Initialize bot
- `/register <wallet>` - Register wallet for monitoring
- `/status` - Show your positions
- `/alerts` - View alert history
- `/thresholds` - Show alert thresholds
- `/help` - Show help

### Alert Thresholds

- 🟡 **WARNING**: < 180% collateral ratio
- 🔴 **CRITICAL**: < 160%
- 💀 **LIQUIDATION**: < 150%

## Project Structure

```
rsk-collateral-monitor/
├── core/                  # Core business logic
│   ├── contract_reader.py    # RSK blockchain interaction
│   └── ratio_calculator.py   # Collateral ratio calculations
├── db/                    # Database layer
│   ├── schema.sql            # SQLite schema
│   └── models.py             # Database operations
├── bot/                   # Telegram bot
│   └── telegram_bot.py       # Bot commands and alerts
├── dashboard/             # Streamlit UI
│   └── app.py                # Main dashboard
├── scripts/               # Scripts and cron jobs
│   ├── poll_positions.py     # Main polling script
│   └── setup_db.py           # Database initialization
├── config/                # Configuration
│   ├── settings.py           # Environment variables
│   └── logging_config.py     # Logging setup
├── data/                  # Database and logs
├── .env                   # Environment variables (create from .env.example)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Configuration

See `.env.example` for all available settings:

```bash
# RSK Configuration
RSK_RPC_URL=https://public-node.rsk.co
RSK_CHAIN_ID=30

# Money on Chain Contracts (VERIFY BEFORE USE)
MOC_PLATFORM_ADDRESS=0x...
MOC_HOLDER_ADDRESS=0x...
DOC_TOKEN_ADDRESS=0x...

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_ADMIN_ID=your_admin_id

# Alert Thresholds
WARNING_THRESHOLD=180
CRITICAL_THRESHOLD=160
LIQUIDATION_THRESHOLD=150

# Polling
POLL_INTERVAL_MINUTES=10
```

## Development

### Run Tests

```bash
pytest tests/
```

### Check Logs

```bash
tail -f data/poller.log
tail -f data/cron.log
```

## Troubleshooting

### "Failed to connect to RSK node"
- Check `RSK_RPC_URL` in `.env`
- Verify network connectivity: `curl https://public-node.rsk.co`

### "Telegram bot not working"
- Verify bot token from @BotFather
- Check bot is not blocked by users

### "No positions found"
- Register wallet via Telegram bot: `/register 0x...`
- Ensure wallet has active positions on Money on Chain

## Safety Notes

⚠️ **Verify Contract Addresses**: The contract addresses in `.env.example` are placeholders. Get official addresses from [Money on Chain documentation](https://moneyonchain.com/).

⚠️ **Not Financial Advice**: This tool provides monitoring only. Always do your own research before making DeFi decisions.

⚠️ **Test First**: Run on testnet or with small positions before relying on alerts.

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or PR.

---

**Built with ❤️ for the Rootstock community**
