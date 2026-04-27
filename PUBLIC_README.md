# ₿ BTC Collateral Monitor

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue)](https://github.com/oVservant/rsk-collateral-monitor)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Telegram Bot](https://img.shields.io/badge/Telegram-@RSKCollateralBot-blue)](https://t.me/RSKCollateralBot)
[![Status](https://img.shields.io/badge/Status-Operational-brightgreen)](https://status.rskcollateral.com)

**Monitor your BTC-backed DeFi positions and get alerts before liquidation.**

---

## 🚀 What is This?

BTC Collateral Monitor is a free service for Rootstock (RSK) DeFi users. It monitors your collateralized positions (like Money on Chain) and sends you Telegram alerts when your collateral ratio approaches dangerous levels.

**Try it now:** [@RSKCollateralBot](https://t.me/RSKCollateralBot)

---

## ⚡ Quick Start

### 1. Start the Bot

1. Open Telegram
2. Go to [@RSKCollateralBot](https://t.me/RSKCollateralBot)
3. Click "Start"

### 2. Register Your Wallet

Send:
```
/register 0xYourWalletAddress
```

### 3. Verify Ownership

Send:
```
/verify
```

Follow the instructions to sign a message with your wallet.

### 4. Done! 🎉

You'll now receive alerts when your collateral ratio drops.

---

## 🎯 Features

### Free Tier

- ✅ **Real-time Monitoring** - Checks every 10 minutes
- ✅ **Telegram Alerts** - Warning, Critical, Liquidation
- ✅ **Position Dashboard** - View your positions anytime
- ✅ **Alert History** - See past alerts
- ✅ **Privacy** - Only you can see your data

### Premium Tier ($5/month)

- ✅ **Multiple Wallets** - Monitor up to 10 wallets
- ✅ **Custom Thresholds** - Set your own alert levels
- ✅ **Faster Polling** - Checks every 5 minutes
- ✅ **Advanced Analytics** - Charts and historical data
- ✅ **Data Export** - CSV, JSON exports
- ✅ **Email Alerts** - In addition to Telegram
- ✅ **Priority Support** - Faster response times

[Upgrade to Premium](https://rskcollateral.com/premium)

---

## 🚨 Alert Levels

| Level | Collateral Ratio | What It Means |
|-------|-----------------|---------------|
| 🟢 Healthy | >180% | Your position is safe |
| 🟡 Warning | 160-180% | Consider adding collateral |
| 🔴 Critical | 150-160% | High risk! Add collateral ASAP |
| 💀 Liquidation | <150% | Position will be liquidated |

**Note:** Liquidation thresholds vary by protocol. Always check your protocol's specific rules.

---

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/register <wallet>` | Register wallet |
| `/verify` | Verify wallet ownership |
| `/status` | Show your positions |
| `/alerts` | Alert history |
| `/thresholds` | Show alert thresholds |
| `/settings` | Notification settings |
| `/help` | Help message |
| `/premium` | Premium features info |

Full documentation: [User Guide](docs/USER_GUIDE.md)

---

## 🔐 Security & Privacy

### We Never Ask For:
- ❌ Private keys
- ❌ Seed phrases
- ❌ Passwords

### We Only Store:
- ✅ Public wallet addresses
- ✅ Telegram ID (for alerts)
- ✅ Position data (from blockchain)

### Security Features:
- 🔒 Message signing for verification
- 🔒 Encrypted connections (HTTPS)
- 🔒 Rate limiting to prevent abuse
- 🔒 Regular security audits

See our [Privacy Policy](docs/USER_GUIDE.md#privacy-policy) for details.

---

## 🛠️ For Developers

This project is **open source**! You can:

### Self-Host Your Own Instance

```bash
git clone https://github.com/oVservant/rsk-collateral-monitor.git
cd rsk-collateral-monitor
make setup
make run-poller
make run-dashboard
```

See [Deployment Guide](docs/DEPLOYMENT.md) for details.

### Contribute

We welcome contributions! See:
- [Contributing Guide](CONTRIBUTING.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Testing Guide](docs/TESTING_GUIDE.md)

### API (Coming Soon)

We're working on a public API for developers. Stay tuned!

---

## 📊 Supported Protocols

Currently supported:
- ✅ **Money on Chain** - BTC-backed stablecoins (DOC, rUSD)

Coming soon:
- 🔄 Other RSK DeFi protocols
- 🔄 Multi-chain support (Ethereum, BSC)

---

## 🙏 Support the Project

This service is free thanks to community support. You can help by:

### Donate

- **BTC:** `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh`
- **RBTC:** `0x1234567890123456789012345678901234567890`
- **USDC (RSK):** `0x1234567890123456789012345678901234567890`

### Spread the Word

- ⭐ Star this repo
- 🐦 Share on Twitter
- 💬 Tell your DeFi friends
- 📝 Write a review

### Contribute Code

- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit PRs
- 📖 Improve docs

---

## 📞 Support

### Get Help

- **Telegram:** [@RSKCollateralSupport](https://t.me/RSKCollateralSupport)
- **Email:** support@rskcollateral.com
- **Docs:** https://docs.rskcollateral.com
- **Status:** https://status.rskcollateral.com

### Report Issues

- **GitHub Issues:** https://github.com/oVservant/rsk-collateral-monitor/issues
- **Bug Bounty:** Up to $100 for critical security bugs (see SECURITY.md)

---

## ⚖️ Legal

### Disclaimer

**This is not financial advice.**

- We provide information, not advice
- DeFi involves significant risk
- You're responsible for your positions
- We're not liable for liquidations or losses

### Terms

By using this service, you agree to our:
- [Terms of Service](docs/USER_GUIDE.md#terms-of-service)
- [Privacy Policy](docs/USER_GUIDE.md#privacy-policy)

---

## 📈 Roadmap

### Q2 2026
- ✅ MVP Launch
- ✅ Telegram bot
- ✅ Basic dashboard
- 🔄 Multi-wallet support

### Q3 2026
- 🔄 Premium tier launch
- 🔄 Advanced analytics
- 🔄 Email alerts
- 🔄 More protocols

### Q4 2026
- 🔄 Public API
- 🔄 Mobile app (iOS/Android)
- 🔄 Multi-chain support
- 🔄 Enterprise features

See full roadmap: [ROADMAP.md](docs/ROADMAP.md)

---

## 🏆 Acknowledgments

Built with:
- [Money on Chain](https://moneyonchain.com/) - DeFi protocol on RSK
- [Rootstock](https://rootstock.io/) - Bitcoin sidechain
- [python-telegram-bot](https://python-telegram-bot.org/) - Bot framework
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Web3.py](https://web3py.readthedocs.io/) - Blockchain interaction

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for the Rootstock community**

**Questions? Feedback?** Reach out: [@RSKCollateralSupport](https://t.me/RSKCollateralSupport)

---

**Tags:** #rootstock #defi #bitcoin #collateral #liquidation #alerts #telegram #opensource
