# Testing Guide

Comprehensive guide for testing BTC Collateral Monitor before production deployment.

## Table of Contents

- [Testing Strategy](#testing-strategy)
- [Unit Tests](#unit-tests)
- [Integration Tests](#integration-tests)
- [Manual Testing](#manual-testing)
- [Test Environment](#test-environment)
- [Test Checklist](#test-checklist)

## Testing Strategy

We use a multi-layered testing approach:

1. **Unit Tests** - Test individual components in isolation
2. **Integration Tests** - Test component interactions
3. **Manual Testing** - Real-world scenario testing
4. **Load Testing** - Performance under stress

## Unit Tests

### Run Unit Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all unit tests
pytest tests/ -v

# Run specific test file
pytest tests/test_contract_reader.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Files

- `tests/test_contract_reader.py` - Contract reader tests
- `tests/test_ratio_calculator.py` - Ratio calculator tests
- `tests/conftest.py` - Pytest fixtures and configuration

### Mocking External Dependencies

Unit tests mock external dependencies:
- RSK RPC node calls
- CoinGecko API
- Telegram Bot API

## Integration Tests

### Run Integration Tests

```bash
# Make sure .env.test is configured
cp .env.test .env

# Run integration tests
python tests/test_integration.py
```

### What Integration Tests Cover

- RSK node connection
- Contract initialization
- Ratio calculations with real prices
- Database operations
- End-to-end polling cycle

### Test Environment Setup

```bash
# Use test database
export DATABASE_PATH=data/test_collateral_monitor.db

# Initialize test database
python scripts/setup_db.py
```

## Manual Testing

### Pre-Deployment Checklist

#### 1. Environment Configuration

```bash
# Validate .env
python scripts/validate_env.py

# Should show:
# ✅ All validations passed!
```

#### 2. Database Setup

```bash
# Initialize database
python scripts/setup_db.py

# Verify tables created
sqlite3 data/collateral_monitor.db ".tables"
```

#### 3. RSK Connection

```bash
# Test connection
python -c "from core.contract_reader import get_contract_reader; print(get_contract_reader().is_connected())"

# Should print: True
```

#### 4. Contract Addresses

- [ ] Verify MOC_PLATFORM_ADDRESS from official docs
- [ ] Verify MOC_HOLDER_ADDRESS from official docs
- [ ] Verify DOC_TOKEN_ADDRESS from official docs
- [ ] Test contract calls with small wallet

#### 5. Telegram Bot

- [ ] Bot responds to `/start`
- [ ] Bot responds to `/help`
- [ ] Bot accepts `/register <wallet>`
- [ ] Bot shows `/status` correctly
- [ ] Test alerts are received

#### 6. Polling Script

```bash
# Run manual poll
python scripts/poll_positions.py

# Check logs
tail -f data/poller.log

# Verify:
# - Connection successful
# - Positions fetched (if any)
# - Snapshots stored
# - No errors
```

#### 7. Dashboard

```bash
# Start dashboard
streamlit run dashboard/app.py

# Open browser: http://localhost:8501

# Verify:
# - Dashboard loads
# - Shows correct number of positions
# - Charts render correctly
# - No console errors
```

#### 8. Cron Job

```bash
# Install cron job
./scripts/install_cron.sh

# Verify installation
crontab -l

# Wait 10 minutes, check logs
tail -f data/cron.log
```

### Test Scenarios

#### Scenario 1: Healthy Position

1. Register wallet with healthy ratio (>180%)
2. Run poll
3. Verify: No alerts sent
4. Check dashboard shows 🟢 status

#### Scenario 2: Warning Alert

1. Simulate or find wallet with ratio <180%
2. Run poll
3. Verify: Warning alert sent via Telegram
4. Check database has alert record
5. Dashboard shows 🟡 status

#### Scenario 3: Critical Alert

1. Simulate or find wallet with ratio <160%
2. Run poll
3. Verify: Critical alert sent via Telegram
4. Dashboard shows 🔴 status

#### Scenario 4: Anomaly Detection

1. Monitor position with sudden ratio drop (>20%)
2. Verify: Anomaly alert sent
3. Check logs for anomaly detection message

#### Scenario 5: Database Backup

```bash
# Run backup
python scripts/backup_db.py

# Verify backup created
ls -lh backups/

# Verify compression
file backups/collateral_monitor_*.db.gz
```

#### Scenario 6: Health Check

```bash
# Run health check
python scripts/health_check.py

# Should show:
# ✅ All checks passed
```

## Load Testing

### Simulate Multiple Positions

```python
# scripts/load_test.py
from db.models import get_database

db = get_database()

# Add 100 test positions
for i in range(100):
    db.add_position(
        position_id=f"test_{i}",
        wallet_address=f"0x{'1'*40}"
    )

print("Added 100 test positions")
```

### Measure Polling Performance

```bash
# Time a polling cycle
time python scripts/poll_positions.py

# Should complete in <30 seconds for 100 positions
```

## Test Checklist

### Before Production

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Environment validation passes
- [ ] RSK connection successful
- [ ] Contract addresses verified
- [ ] Telegram bot works
- [ ] Polling runs without errors
- [ ] Dashboard displays correctly
- [ ] Cron job installed and running
- [ ] Health check passes
- [ ] Backup script works
- [ ] Logs are rotating
- [ ] No memory leaks (run for 24h)
- [ ] Alert thresholds are correct
- [ ] Multi-user support tested (if applicable)

### After Deployment

- [ ] First poll successful
- [ ] First alert received (test with low threshold)
- [ ] Dashboard accessible
- [ ] Logs being written
- [ ] Database growing normally
- [ ] No unexpected errors in logs
- [ ] Cron job running on schedule
- [ ] Health checks passing

## Troubleshooting Failed Tests

### "Failed to connect to RSK node"

```bash
# Check network
curl https://public-node.rsk.co

# Try alternative RPC
export RSK_RPC_URL=https://rpc.rsk.co
```

### "Contract not initialized"

- Verify contract addresses in `.env`
- Check addresses are 42 characters starting with 0x
- Ensure addresses are from official source

### "Telegram bot not working"

- Verify bot token from @BotFather
- Check bot is not blocked
- Test with simple message first

### "Database locked"

```bash
# Check for running processes
ps aux | grep sqlite

# Kill if necessary
pkill -f sqlite

# Or wait for process to complete
```

## Continuous Testing

### CI/CD Pipeline

GitHub Actions runs tests automatically:
- On every push to main
- On every pull request
- Tests: Python 3.10, 3.11, 3.12
- Linting: flake8, black, isort
- Security: safety check

### Monitoring Test Coverage

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# Open in browser
open htmlcov/index.html

# Target: >80% coverage
```

---

**Last Updated:** 2026-04-27  
**Version:** 1.0.0
