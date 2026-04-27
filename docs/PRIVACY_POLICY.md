# Privacy Policy

**Effective Date:** 2026-04-27  
**Service:** BTC Collateral Monitor  
**Contact:** support@rskcollateral.com

---

## 📋 Overview

BTC Collateral Monitor is an open-source service that monitors BTC-backed DeFi positions on Rootstock blockchain and sends alerts via Telegram.

This Privacy Policy explains what data we collect, how we use it, and your rights.

---

## 🔍 What Data We Collect

### Information You Provide

| Data Type | Purpose | Retention |
|-----------|---------|-----------|
| **Telegram ID** | Send you alerts | While account is active |
| **Wallet Address** | Monitor positions | While account is active |
| **Notification Preferences** | Customize alerts | While account is active |

### Information We Automatically Collect

| Data Type | Purpose | Retention |
|-----------|---------|-----------|
| **Position Data** | From blockchain (public) | 90 days |
| **Alert History** | Track sent alerts | 90 days |
| **Usage Logs** | Prevent abuse, debugging | 30 days |

### What We NEVER Collect

- ❌ Private keys
- ❌ Seed phrases
- ❌ Passwords
- ❌ Email addresses (unless you opt-in for premium features)
- ❌ Personal identification documents
- ❌ Financial information beyond wallet addresses

---

## 🎯 How We Use Your Data

### Primary Uses

1. **Service Delivery**
   - Monitor your positions
   - Send you alerts
   - Display your dashboard

2. **Security**
   - Verify wallet ownership
   - Prevent abuse and spam
   - Detect unauthorized access

3. **Improvement**
   - Analyze usage patterns (anonymized)
   - Fix bugs
   - Add requested features

### What We DON'T Do

- ❌ Sell your data to third parties
- ❌ Share your data with advertisers
- ❌ Use your data for marketing without consent
- ❌ Track you across other websites/apps
- ❌ Profile you for financial products

---

## 🔐 Data Security

### Technical Measures

- 🔒 **Encryption in Transit** - All data uses HTTPS/TLS
- 🔒 **Encryption at Rest** - Database encrypted on disk
- 🔒 **Access Controls** - Only authorized developers can access production data
- 🔒 **Rate Limiting** - Prevents abuse and DDoS attacks
- 🔒 **Regular Audits** - Security reviews of code and infrastructure

### Wallet Verification

We use **message signing** to verify wallet ownership:
- No private keys are transmitted
- No transactions are sent
- No gas fees are charged
- Signature is verified and discarded

---

## 📢 Data Sharing

### When We Share Data

We **never** sell or rent your data. We only share in these limited cases:

1. **Service Providers**
   - Hosting providers (e.g., DigitalOcean)
   - Telegram (for bot functionality)
   - Blockchain nodes (public data only)

2. **Legal Requirements**
   - If required by law
   - To protect our rights
   - To prevent fraud or abuse

3. **With Your Consent**
   - You explicitly authorize sharing
   - You can revoke consent anytime

### Public Data

Wallet addresses and positions are:
- ✅ Already public on the blockchain
- ✅ Visible only to you in our dashboard
- ✅ Never linked to your identity publicly

---

## 👤 Your Rights

You have the right to:

### Access
Request a copy of your data anytime:
```
/export_data
```

### Correction
Update your wallet or preferences:
```
/register <new_wallet>
/settings
```

### Deletion
Delete your account and all data:
```
/delete_account
```

### Portability
Export your data in machine-readable format (CSV, JSON):
```
/export csv
/export json
```

### Opt-Out
Stop receiving non-essential communications:
```
/settings
# Toggle notifications off
```

---

## 📅 Data Retention

### Active Accounts

Data is retained while your account is active:
- Telegram ID: Indefinitely
- Wallet addresses: Indefinitely
- Position history: 90 days rolling
- Alert history: 90 days rolling

### Inactive Accounts

If you don't interact with the bot for **12 months**:
- We'll send a reminder
- If no response, account is deleted
- All data is permanently removed

### Backups

- Database backups: 30 days
- Log backups: 7 days
- After deletion, data may persist in backups until rotation

---

## 🌍 International Data Transfers

### Where We Store Data

- **Primary:** European Union (GDPR compliant)
- **Backup:** European Union
- **Service Providers:** May vary (all GDPR-compliant)

### Your Location

Our service is available worldwide. By using our service, you consent to data processing in the jurisdictions where we operate.

---

## 🧒 Children's Privacy

Our service is **not intended for children under 18**.

We don't knowingly collect data from children. If we discover we have, we'll delete it immediately.

---

## 🔄 Changes to This Policy

We may update this Privacy Policy:
- When laws change
- When we add new features
- When we improve our practices

### How We Notify You

- **Minor changes:** Updated date on this page
- **Major changes:** Bot notification to all users
- **Material changes:** 30 days notice before生效

### Your Continued Use

Continuing to use our service after changes constitutes acceptance of the new policy.

---

## 📞 Contact Us

### Privacy Questions

- **Email:** privacy@rskcollateral.com
- **Telegram:** @RSKCollateralSupport
- **GitHub:** https://github.com/oVservant/rsk-collateral-monitor/issues

### Data Protection Officer

For EU users, you can contact our DPO at:
- **Email:** dpo@rskcollateral.com

### Complaints

If you're not satisfied with our response, you can complain to:
- Your local data protection authority
- Irish Data Protection Commission (if in EU)

---

## ⚖️ Legal Basis for Processing (GDPR)

We process your data under these legal bases:

1. **Contractual Necessity**
   - To provide the service you requested
   - To fulfill our terms of service

2. **Legitimate Interests**
   - Security and fraud prevention
   - Service improvement
   - Communication about updates

3. **Consent**
   - Optional features (email alerts, analytics)
   - You can withdraw consent anytime

---

## 🇺🇸 California Privacy Rights (CCPA)

If you're a California resident, you have additional rights:

### Right to Know

Request what personal information we've collected in the past 12 months.

### Right to Delete

Request deletion of your personal information.

### Right to Opt-Out

We don't sell personal information, so this doesn't apply.

### Non-Discrimination

We won't discriminate if you exercise your privacy rights.

### How to Exercise

Email: privacy@rskcollateral.com with subject "CCPA Request"

---

## 🇪🇺 EU Privacy Rights (GDPR)

If you're in the EU, you have these rights:

- Right to access
- Right to rectification
- Right to erasure ("right to be forgotten")
- Right to restrict processing
- Right to data portability
- Right to object
- Rights regarding automated decision-making

### How to Exercise

Email: privacy@rskcollateral.com with subject "GDPR Request"

---

## 📚 Additional Resources

### Learn More About Privacy

- [GDPR Overview](https://gdpr.eu/)
- [CCPA Overview](https://oag.ca.gov/privacy/ccpa)
- [Crypto Privacy Best Practices](https://privacyinternational.org/)

### Our Other Policies

- [Terms of Service](USER_GUIDE.md#terms-of-service)
- [Security Policy](../SECURITY.md)
- [Cookie Policy](#cookies)

---

## 🍪 Cookies

### What We Use

Our dashboard uses:
- **Session cookies** - Keep you logged in (deleted when you close browser)
- **Analytics cookies** - Anonymous usage statistics (opt-in)

### Your Choices

- Block cookies in browser settings
- Use bot-only mode (no dashboard, no cookies)
- Clear cookies anytime

---

## 🛡️ Data Breach Response

### If We Have a Breach

We'll notify you within **72 hours** if:
- Your data is compromised
- There's risk to your rights
- We're legally required to notify

### What We'll Tell You

- What happened
- What data was affected
- What we're doing about it
- What you can do to protect yourself

---

## 🏛️ Regulatory Compliance

### GDPR (EU)

We comply with the General Data Protection Regulation:
- Lawful basis for processing
- Data minimization
- Purpose limitation
- Storage limitation
- Integrity and confidentiality

### CCPA (California)

We comply with the California Consumer Privacy Act:
- Right to know
- Right to delete
- Non-discrimination

### LGPD (Brazil)

We comply with Brazil's Lei Geral de Proteção de Dados.

---

**Last Updated:** 2026-04-27  
**Version:** 1.0.0

**Tags:** #privacy #gdpr #ccpa #data-protection #opensource
