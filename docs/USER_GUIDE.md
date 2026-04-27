# BTC Collateral Monitor - User Guide

**Bot de Telegram:** @RSKCollateralBot  
**Dashboard:** https://rskcollateral.com  
**Status:** https://status.rskcollateral.com

---

## 🚀 Quick Start

### 1. Start the Bot

1. Open Telegram
2. Search for `@RSKCollateralBot`
3. Click "Start" or send `/start`

### 2. Register Your Wallet

```
/register 0x1234567890123456789012345678901234567890
```

Replace with your actual wallet address.

### 3. Verify Ownership (Required)

```
/verify
```

The bot will send you a message to sign with your wallet. Sign it and send back the signature:

```
/verify 0xabc123...signature
```

### 4. You're Done! 🎉

The bot will now monitor your positions and send alerts when collateral ratios approach liquidation.

---

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and help |
| `/register <wallet>` | Register wallet for monitoring |
| `/verify` | Verify wallet ownership |
| `/status` | Show your positions and ratios |
| `/alerts` | View alert history |
| `/thresholds` | Show alert thresholds |
| `/settings` | Configure notification preferences |
| `/help` | Show help message |

---

## 🚨 Alert Thresholds

| Level | Ratio | Action |
|-------|-------|--------|
| 🟢 **Healthy** | >180% | No action needed |
| 🟡 **Warning** | 160-180% | Consider adding collateral |
| 🔴 **Critical** | 150-160% | High risk, add collateral ASAP |
| 💀 **Liquidation** | <150% | Position will be liquidated |

**Note:** Thresholds may vary by protocol. Always check your protocol's specific liquidation threshold.

---

## 💡 Best Practices

### 1. Monitor Regularly

Check your positions daily, especially during market volatility.

### 2. Set Conservative Thresholds

Don't wait until you're at 160%. Add collateral at 180-200% to be safe.

### 3. Enable All Notifications

Make sure you receive all alert types:
```
/settings
# Enable: warning, critical, liquidation
```

### 4. Have RBTC Ready

Keep some RBTC in your wallet to add collateral quickly if needed.

### 5. Understand the Risks

- Market volatility can cause rapid ratio changes
- Liquidations are automatic and irreversible
- This tool provides alerts, not financial advice

---

## ❓ FAQ

### How often do you check my positions?

We check every 10 minutes. Premium users can get 5-minute checks.

### Is this service free?

Yes! Basic monitoring is completely free. We also offer premium features for power users.

### What protocols do you support?

Currently we support:
- ✅ Money on Chain (MoC)
- 🔄 More protocols coming soon

### Can I monitor multiple wallets?

Free tier: 1 wallet  
Premium tier: Up to 10 wallets

### How do I stop receiving alerts?

You can:
- Pause alerts: `/settings` → Toggle notifications off
- Unregister wallet: `/unregister <wallet>`
- Block the bot (not recommended)

### Is my data private?

Yes! Your wallet addresses and positions are:
- ✅ Only visible to you
- ✅ Never shared with third parties
- ✅ Stored securely
- ✅ Deleted when you unregister

### What if I get liquidated anyway?

We provide alerts as early warning, but:
- We're not responsible for liquidations
- Market can move faster than alerts
- Always do your own risk management
- Consider over-collateralizing

### Can I export my data?

Yes! Premium users can export:
- Position history (CSV, JSON)
- Alert history
- Analytics reports

Use: `/export <format>`

---

## 🔐 Security

### How do you verify my wallet?

We use **message signing** (no gas fees):
1. Bot generates unique nonce
2. You sign message with your wallet
3. We verify signature matches wallet
4. No transaction needed, no private keys shared

### Do you store my private keys?

**NO!** We never ask for or store:
- ❌ Private keys
- ❌ Seed phrases
- ❌ Passwords

Only public wallet addresses are stored.

### Is the dashboard secure?

Yes! We use:
- 🔒 HTTPS encryption
- 🔒 Telegram authentication
- 🔒 Session management
- 🔒 Rate limiting

---

## 🆘 Troubleshooting

### "Wallet address invalid"

Make sure:
- Address starts with `0x`
- Address is 42 characters long
- No typos or extra spaces

Example: `0x1234567890123456789012345678901234567890`

### "Verification failed"

Try again:
1. Make sure you're signing the exact message shown
2. Use the same wallet you registered
3. Complete within 10 minutes (nonce expires)
4. Send full signature (0x...)

### "No positions found"

Possible reasons:
- Wallet has no open positions in supported protocols
- Position not yet detected (wait 10 minutes)
- Wrong wallet address registered

Check with: `/status`

### Not receiving alerts

Check:
1. Bot is not blocked
2. Notifications enabled: `/settings`
3. Wallet has active positions
4. Check spam folder (Telegram sometimes filters)

### Dashboard not loading

Try:
1. Refresh browser (Ctrl+R)
2. Clear cache
3. Check status page: https://status.rskcollateral.com
4. Contact support if issue persists

---

## 📞 Support

### Get Help

- **Telegram:** @RSKCollateralSupport
- **Email:** support@rskcollateral.com
- **Docs:** https://docs.rskcollateral.com
- **Status:** https://status.rskcollateral.com

### Report Bugs

Found a bug? Report it:
- GitHub Issues: https://github.com/oVservant/rsk-collateral-monitor/issues
- Telegram: @RSKCollateralSupport

### Feature Requests

Want a new feature?
- Vote on existing: https://github.com/oVservant/rsk-collateral-monitor/discussions
- Submit new: https://github.com/oVservant/rsk-collateral-monitor/discussions/new

---

## 📈 Premium Features

Upgrade to Premium for:
- ✅ Multiple wallets (up to 10)
- ✅ Custom alert thresholds
- ✅ Faster polling (every 5 min)
- ✅ Advanced analytics dashboard
- ✅ Data export (CSV, JSON)
- ✅ Email alerts
- ✅ Priority support

**Pricing:**
- Monthly: $5/month
- Yearly: $50/year (save 17%)

Upgrade: `/premium`

---

## 🙏 Donations

This service is free thanks to community support. If you find it useful, consider donating:

**BTC:** `bc1q...`  
**RBTC:** `0x...`  
**USDC (RSK):** `0x...`

Donations help cover server costs and development.

---

## ⚖️ Terms of Service

### Important Disclaimers

1. **Not Financial Advice**
   - This tool provides information, not advice
   - Always do your own research
   - Consult financial advisors for investment decisions

2. **No Guarantees**
   - We strive for accuracy but don't guarantee it
   - Alerts may be delayed or fail
   - We're not responsible for liquidations

3. **Use at Your Own Risk**
   - DeFi involves significant risk
   - You're responsible for your positions
   - Never invest more than you can afford to lose

4. **Data Privacy**
   - We respect your privacy
   - See Privacy Policy for details
   - You can delete your data anytime

### Acceptable Use

You agree NOT to:
- Abuse the service (spam, attacks)
- Reverse engineer the code
- Resell the service
- Use for illegal activities

Violations may result in account suspension.

---

## 🔒 Privacy Policy

### What We Collect

- Telegram ID (for bot communication)
- Wallet addresses (public, no private keys)
- Position data (from blockchain)
- Alert preferences

### How We Use It

- Send you alerts
- Display your dashboard
- Improve the service
- Prevent abuse

### What We Don't Do

- ❌ Sell your data
- ❌ Share with third parties (except as required by law)
- ❌ Use for marketing without consent
- ❌ Store private keys or sensitive info

### Your Rights

You can:
- ✅ Access your data anytime
- ✅ Delete your data (`/delete_account`)
- ✅ Export your data (Premium)
- ✅ Opt-out of non-essential communications

### Data Retention

- Active users: Data kept while account is active
- Inactive accounts: Deleted after 12 months
- Backups: Kept for 30 days

---

## 📚 Resources

### Learn More

- [What is Collateral Ratio?](https://docs.moneyonchain.com/collateral)
- [How to Avoid Liquidations](https://rootstock.io/blog/defi-risk-management)
- [Rootstock DeFi Guide](https://rootstock.io/defi)

### Tools

- [RSK Block Explorer](https://rootstock.blockscout.com/)
- [Money on Chain Dashboard](https://app.moneyonchain.com/)
- [RBTC Price](https://www.coingecko.com/en/coins/rsk-infrastructure-framework)

---

**Last Updated:** 2026-04-27  
**Version:** 1.0.0

**Tags:** #userguide #documentation #telegram #defi #rootstock
