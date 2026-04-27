# Deployment Guide

## Option 1: Docker Compose (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- `.env` file configured

### Steps

```bash
# Build images
docker-compose build

# Start dashboard only
docker-compose up -d dashboard

# Test polling manually
docker-compose run --rm poller python scripts/poll_positions.py

# View logs
docker-compose logs -f poller
docker-compose logs -f dashboard
```

**Access Dashboard:** `http://localhost:8501`

---

## Option 2: Direct Installation (VPS)

### Prerequisites
- Python 3.10+
- pip
- Cron daemon

### Steps

```bash
# Navigate to project
cd /home/ovservant/projects/rsk-collateral-monitor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
nano .env  # Edit settings

# Initialize database
python scripts/setup_db.py

# Test polling
python scripts/poll_positions.py

# Set up cron job
crontab -e
# Add: */10 * * * * cd /home/ovservant/projects/rsk-collateral-monitor && source venv/bin/activate && python scripts/poll_positions.py >> data/cron.log 2>&1

# Start dashboard (background)
nohup streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0 > data/dashboard.log 2>&1 &
```

**Access Dashboard:** `http://your-vps-ip:8501`

---

## Option 3: Systemd Service (Production)

### Poller Service

Create `/etc/systemd/system/rsk-poller.service`:

```ini
[Unit]
Description=RSK Collateral Monitor Poller
After=network.target

[Service]
Type=oneshot
User=ovservant
WorkingDirectory=/home/ovservant/projects/rsk-collateral-monitor
Environment="PATH=/home/ovservant/projects/rsk-collateral-monitor/venv/bin"
ExecStart=/home/ovservant/projects/rsk-collateral-monitor/venv/bin/python scripts/poll_positions.py
StandardOutput=append:/home/ovservant/projects/rsk-collateral-monitor/data/poller.log
StandardError=append:/home/ovservant/projects/rsk-collateral-monitor/data/poller.log
```

### Dashboard Service

Create `/etc/systemd/system/rsk-dashboard.service`:

```ini
[Unit]
Description=RSK Collateral Monitor Dashboard
After=network.target

[Service]
Type=simple
User=ovservant
WorkingDirectory=/home/ovservant/projects/rsk-collateral-monitor
Environment="PATH=/home/ovservant/projects/rsk-collateral-monitor/venv/bin"
ExecStart=/home/ovservant/projects/rsk-collateral-monitor/venv/bin/streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

### Enable Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable rsk-poller.timer  # Create timer for cron-like scheduling
sudo systemctl enable rsk-dashboard
sudo systemctl start rsk-dashboard

# Check status
sudo systemctl status rsk-dashboard
sudo systemctl status rsk-poller
```

---

## Cron Job Setup

### Edit Crontab

```bash
crontab -e
```

### Add Entry

```bash
# RSK Collateral Monitor - Poll every 10 minutes
*/10 * * * * cd /home/ovservant/projects/rsk-collateral-monitor && source venv/bin/activate && python scripts/poll_positions.py >> data/cron.log 2>&1

# Optional: Restart dashboard daily at 3 AM
0 3 * * * pkill -f "streamlit run" && sleep 5 && cd /home/ovservant/projects/rsk-collateral-monitor && source venv/bin/activate && nohup streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0 > data/dashboard.log 2>&1 &
```

### Verify Cron

```bash
# List cron jobs
crontab -l

# Check cron logs
grep CRON /var/log/syslog | tail -20
```

---

## Nginx Reverse Proxy (Optional)

For production dashboard access with HTTPS:

### Install Nginx

```bash
sudo apt update
sudo apt install nginx
```

### Configure

Create `/etc/nginx/sites-available/rsk-monitor`:

```nginx
server {
    listen 80;
    server_name monitor.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Enable and Get SSL

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/rsk-monitor /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Get SSL certificate (Certbot)
sudo certbot --nginx -d monitor.yourdomain.com
```

---

## Monitoring

### Health Check Script

Create `scripts/health_check.py`:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
import sqlite3

project_root = Path(__file__).parent.parent
db_path = project_root / 'data' / 'collateral_monitor.db'

# Check database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM positions")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"✅ Database OK - {count} positions")
except Exception as e:
    print(f"❌ Database error: {e}")
    sys.exit(1)

# Check last poll
log_file = project_root / 'data' / 'poller.log'
if log_file.exists():
    with open(log_file) as f:
        lines = f.readlines()
        if lines and "Poll completed" in lines[-1]:
            print("✅ Last poll successful")
        else:
            print("⚠️ Check poller logs")
else:
    print("⚠️ No poller logs found")

print("✅ Health check passed")
```

### Add to Cron

```bash
# Health check every hour
0 * * * * cd /home/ovservant/projects/rsk-collateral-monitor && python scripts/health_check.py >> data/health.log 2>&1
```

---

## Backup Strategy

### Database Backup

```bash
# Daily backup (add to crontab)
0 2 * * * cp /home/ovservant/projects/rsk-collateral-monitor/data/collateral_monitor.db /home/ovservant/backups/rsk-monitor-$(date +\%Y\%m\%d).db

# Weekly backup to remote
0 3 * * 0 rsync -avz /home/ovservant/backups/rsk-monitor-*.db user@backup-server:/backups/
```

### Configuration Backup

```bash
# Backup .env (encrypted)
tar -czf env-backup-$(date +\%Y\%m\%d).tar.gz .env
gpg -c env-backup-*.tar.gz
```

---

## Troubleshooting

### Dashboard Not Accessible

```bash
# Check if Streamlit is running
ps aux | grep streamlit

# Check port
netstat -tlnp | grep 8501

# Restart
sudo systemctl restart rsk-dashboard
# Or: docker-compose restart dashboard
```

### Poller Not Running

```bash
# Check cron logs
grep CRON /var/log/syslog | grep poll_positions

# Manual test
python scripts/poll_positions.py

# Check logs
tail -f data/poller.log
```

### Database Errors

```bash
# Check database integrity
sqlite3 data/collateral_monitor.db "PRAGMA integrity_check;"

# Backup and recreate
cp data/collateral_monitor.db data/collateral_monitor.db.bak
python scripts/setup_db.py
```

---

## Production Checklist

- [ ] `.env` configured with production values
- [ ] Contract addresses verified from official source
- [ ] Telegram bot token secured
- [ ] Database backups configured
- [ ] Monitoring/health checks in place
- [ ] Log rotation configured
- [ ] Firewall rules (only 8501 open for dashboard)
- [ ] SSL certificate for dashboard (if using domain)
- [ ] Tested alert delivery
- [ ] Documented runbook for issues

---

**Last Updated:** 2026-04-27
