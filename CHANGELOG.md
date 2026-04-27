# Changelog

All notable changes to BTC Collateral Monitor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Multi-user Telegram alert support
- Price oracle integration (Chainlink or similar)
- Batch RPC calls for gas optimization
- Enhanced dashboard with charts and analytics
- Docker production deployment guide
- GitHub Actions CI/CD pipeline

### Under Consideration
- Support for multiple DeFi protocols (in addition to Money on Chain)
- Webhook notifications (in addition to Telegram)
- Mobile app for monitoring
- Historical data export functionality

---

## [1.0.0] - 2026-04-27

### Added

#### Core Functionality
- **Contract Reader**: Web3.py integration for RSK blockchain
- **Ratio Calculator**: Real-time collateral ratio calculations
- **Threshold Monitoring**: Warning (<180%), Critical (<160%), Liquidation (<150%)
- **Telegram Bot**: Alert notifications via Telegram
- **Streamlit Dashboard**: Web UI for monitoring positions

#### Database
- SQLite schema for users, positions, snapshots, and alerts
- Historical data tracking
- Alert history management

#### DevOps
- Docker and Docker Compose configuration
- Cron job installation script
- Deployment guide for VPS and Docker
- Integration tests

#### Documentation
- README with quick start guide
- Technical architecture documentation
- Deployment guide
- Next steps checklist
- Contributing guidelines
- Code of conduct
- Security policy

### Technical Details
- **Lines of Code**: ~2,600+
- **Files**: 32
- **Python Version**: 3.10+
- **Dependencies**: web3.py, python-telegram-bot, streamlit, requests

### Infrastructure
- RSK Public RPC node integration
- CoinGecko price API integration
- Telegram Bot API integration

---

## Versioning

We use [Semantic Versioning](https://semver.org/):

* **MAJOR** version for incompatible changes
* **MINOR** version for backwards-compatible features
* **PATCH** version for backwards-compatible bug fixes

---

**Initial Release** 🎉
