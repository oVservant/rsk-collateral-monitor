# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of BTC Collateral Monitor seriously. If you believe you've found a security vulnerability, please follow these guidelines:

### How to Report

* **DO NOT** open a public GitHub issue for security vulnerabilities
* Email your findings to: matiasfleker@gmail.com
* Include as much information as possible:
  - Description of the vulnerability
  - Steps to reproduce
  - Potential impact
  - Suggested fix (if any)

### What to Expect

* **Initial Response:** Within 48 hours
* **Status Update:** Within 1 week
* **Resolution:** Depends on severity, typically within 2-4 weeks

### Security Best Practices

#### For Users

1. **Protect your API keys**
   - Never commit `.env` files to Git
   - Use environment variables for sensitive data
   - Rotate Telegram bot tokens if compromised

2. **Verify contract addresses**
   - Always verify Money on Chain contract addresses from official sources
   - Check https://docs.moneyonchain.com/ for latest addresses

3. **Monitor logs**
   - Regularly check `data/poller.log` for unusual activity
   - Set up alerts for failed polls

4. **Keep dependencies updated**
   - Regularly run `pip install --upgrade -r requirements.txt`
   - Monitor security advisories for dependencies

#### For Contributors

1. **No sensitive data in code**
   - Never commit API keys, tokens, or passwords
   - Use `.env.example` for configuration templates

2. **Input validation**
   - Validate all user inputs (wallet addresses, etc.)
   - Sanitize data before database operations

3. **Secure dependencies**
   - Pin dependency versions in `requirements.txt`
   - Review security advisories for dependencies

## Security Measures in Place

* Environment variables for sensitive configuration
* Input validation for wallet addresses
* SQLite parameterized queries (SQL injection protection)
* Rate limiting considerations for Telegram bot
* Read-only blockchain operations (no private keys stored)

## Known Limitations

* Uses public RSK RPC node (rate limited)
* Relies on CoinGecko API for price data (external dependency)
* Telegram bot token must be stored securely by user

---

**Thank you for helping keep BTC Collateral Monitor secure!** 🔒
