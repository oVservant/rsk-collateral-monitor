#!/usr/bin/env python3
"""
BTC Collateral Monitor - Streamlit Dashboard

Run with:
    streamlit run dashboard/app.py
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from db.models import get_database
from core.ratio_calculator import get_ratio_calculator

# Page config
st.set_page_config(
    page_title="BTC Collateral Monitor",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #f7931a;
}
.warning { border-left-color: #ffaa00; }
.critical { border-left-color: #ff4444; }
.ok { border-left-color: #00ff00; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("₿ BTC Collateral Monitor")
st.markdown("**Money on Chain** positions on Rootstock")

# Initialize database
db = get_database()
ratio_calc = get_ratio_calculator()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Quick stats
    positions = db.get_active_positions()
    st.metric("Active Positions", len(positions))
    
    # Get current RBTC price
    rbtc_price = ratio_calc.get_rbtc_price_usd()
    st.metric("RBTC Price", f"${rbtc_price:,.2f}")
    
    st.divider()
    
    # Thresholds info
    st.subheader("Alert Thresholds")
    st.info(f"""
    🟡 Warning: < {settings.WARNING_THRESHOLD}%
    
    🔴 Critical: < {settings.CRITICAL_THRESHOLD}%
    
    💀 Liquidation: < {settings.LIQUIDATION_THRESHOLD}%
    """)
    
    st.divider()
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# Main content
if not positions:
    st.warning("📭 No active positions being monitored.")
    st.info("Register wallets via the Telegram bot: `@your_bot_name`")
    st.stop()

# Positions table
st.subheader("📊 Active Positions")

# Build positions data
positions_data = []
for pos in positions:
    history = db.get_position_history(pos['position_id'], limit=1)
    if history:
        snapshot = history[0]
        ratio = snapshot['collateral_ratio']
        
        # Determine status
        if ratio < settings.LIQUIDATION_THRESHOLD:
            status = "💀 LIQUIDATION"
            status_color = "critical"
        elif ratio < settings.CRITICAL_THRESHOLD:
            status = "🔴 CRITICAL"
            status_color = "critical"
        elif ratio < settings.WARNING_THRESHOLD:
            status = "🟡 WARNING"
            status_color = "warning"
        else:
            status = "🟢 OK"
            status_color = "ok"
        
        positions_data.append({
            "Position ID": pos['position_id'],
            "Wallet": f"{pos['wallet_address'][:8]}...{pos['wallet_address'][-6:]}",
            "Ratio": f"{ratio:.2f}%",
            "Status": status,
            "Collateral (RBTC)": f"{float(snapshot['collateral_amount']) / 1e18:.4f}",
            "Debt (DOC)": f"{float(snapshot['debt_amount']) / 1e18:.2f}",
            "Updated": snapshot['snapshot_timestamp']
        })

if positions_data:
    df = pd.DataFrame(positions_data)
    
    # Color-code status column
    def color_status(val):
        if "LIQUIDATION" in val:
            return "color: #ff4444; font-weight: bold"
        elif "CRITICAL" in val:
            return "color: #ff4444"
        elif "WARNING" in val:
            return "color: #ffaa00"
        else:
            return "color: #00ff00"
    
    styled_df = df.style.applymap(color_status, subset=["Status"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
else:
    st.info("No position data available yet. Run the polling script first.")

# Position details
if positions_data:
    st.divider()
    st.subheader("📈 Position History")
    
    # Select position
    position_options = {f"#{p['position_id']}": p['Position ID'] for p in positions_data}
    selected = st.selectbox("Select Position", list(position_options.keys()))
    
    if selected:
        pos_id = position_options[selected]
        history = db.get_position_history(pos_id, limit=50)
        
        if history:
            # Create history dataframe
            hist_data = []
            for snap in reversed(history):  # Oldest first
                hist_data.append({
                    "Timestamp": snap['snapshot_timestamp'],
                    "Ratio": snap['collateral_ratio'],
                    "RBTC Price": snap['rbtc_price_usd']
                })
            
            hist_df = pd.DataFrame(hist_data)
            
            # Plot ratio over time
            st.line_chart(hist_df.set_index("Timestamp")[["Ratio"]])
            
            # Show threshold lines
            st.markdown(f"""
            **Thresholds:**
            - Warning: {settings.WARNING_THRESHOLD}%
            - Critical: {settings.CRITICAL_THRESHOLD}%
            - Liquidation: {settings.LIQUIDATION_THRESHOLD}%
            """)

# Recent alerts
st.divider()
st.subheader("🔔 Recent Alerts")

alerts = db.get_unsent_alerts()
if alerts:
    for alert in alerts[:5]:
        emoji = "🔴" if alert['alert_type'] == "CRITICAL" else "⚠️"
        st.warning(f"""
        {emoji} **{alert['alert_type']}** - Position #{alert['position_id']}
        
        Ratio: {alert['collateral_ratio']:.2f}% | Time: {alert['created_at']}
        """)
else:
    st.success("✅ No pending alerts!")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
BTC Collateral Monitor | Money on Chain | Rootstock
</div>
""", unsafe_allow_html=True)
