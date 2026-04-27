# Contributing to BTC Collateral Monitor

First off, thank you for considering contributing to BTC Collateral Monitor! It's people like you that make this tool great for the Rootstock community.

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed and what behavior you expected**
* **Include screenshots if possible**
* **Include environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List some examples of how this enhancement would be used**

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include tests if applicable
* Update documentation as needed
* Make sure your code passes linting and tests

## Development Setup

### Prerequisites

* Python 3.10+
* pip
* Git

### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/rsk-collateral-monitor.git
cd rsk-collateral-monitor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if you add them)
# pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run integration tests
python tests/test_integration.py

# Run all tests (if you add pytest)
pytest tests/
```

### Code Style

* Follow PEP 8 guidelines
* Use type hints where possible
* Write docstrings for public functions
* Keep functions small and focused

## Project Structure

```
rsk-collateral-monitor/
├── core/                    # Core business logic
│   ├── contract_reader.py   # RSK blockchain interaction
│   └── ratio_calculator.py  # Collateral ratio calculations
├── db/                      # Database layer
│   ├── schema.sql           # SQLite schema
│   └── models.py            # Database operations
├── bot/                     # Telegram bot
│   └── telegram_bot.py      # Bot commands and alerts
├── dashboard/               # Streamlit UI
│   └── app.py               # Main dashboard
├── scripts/                 # Scripts and cron jobs
│   ├── poll_positions.py    # Main polling script
│   └── setup_db.py          # Database initialization
├── config/                  # Configuration
│   ├── settings.py          # Environment variables
│   └── logging_config.py    # Logging setup
├── tests/                   # Test suite
│   └── test_integration.py  # Integration tests
└── docs/                    # Documentation
    ├── ARCHITECTURE.md      # Technical architecture
    └── DEPLOYMENT.md        # Deployment guide
```

## Architecture Overview

The system consists of four main components:

1. **Contract Reader** - Fetches position data from Money on Chain contracts on RSK
2. **Ratio Calculator** - Calculates collateral ratios and checks thresholds
3. **Telegram Bot** - Sends alerts to users
4. **Dashboard** - Streamlit web UI for monitoring

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed technical documentation.

## Deployment

For deployment instructions, see [DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Questions?

Feel free to open an issue for any questions or discussions.

---

**Thank you for contributing!** 🎉
