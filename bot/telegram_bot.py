"""Telegram bot for BTC Collateral Monitor alerts."""
import logging
from typing import Optional
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

from config.settings import settings
from db.models import get_database

logger = logging.getLogger('collateral_monitor.bot')


class CollateralBot:
    """Telegram bot for sending collateral alerts."""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.admin_id = settings.TELEGRAM_ADMIN_ID
        self.db = get_database()
        self.bot = Bot(token=self.token) if self.token else None
        self.application = None
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user
        telegram_id = str(user.id)
        
        # Register user in database
        self.db.add_user(
            telegram_id=telegram_id,
            username=user.username
        )
        
        welcome_msg = """
👋 Welcome to BTC Collateral Monitor!

I'll alert you when your BTC-backed positions approach liquidation.

Commands:
/register <wallet> - Register wallet for monitoring
/status - Show your positions
/alerts - View alert history
/thresholds - Show alert thresholds
/help - Show this help

Example:
/register 0x1234...5678
"""
        
        await update.message.reply_text(welcome_msg.strip())
        logger.info(f"User {telegram_id} started bot")
    
    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /register command."""
        telegram_id = str(update.effective_user.id)
        
        if not context.args:
            await update.message.reply_text("Usage: /register <wallet_address>")
            return
        
        wallet = context.args[0]
        
        # Validate wallet address (basic check)
        if not wallet.startswith('0x') or len(wallet) != 42:
            await update.message.reply_text("❌ Invalid wallet address format")
            return
        
        # Update user in database
        self.db.add_user(telegram_id=telegram_id, wallet=wallet)
        
        await update.message.reply_text(
            f"✅ Wallet registered: `{wallet[:10]}...{wallet[-8:]}`\n\n"
            f"I'll monitor positions for this address and send alerts.",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {telegram_id} registered wallet {wallet[:10]}...")
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        telegram_id = str(update.effective_user.id)
        user = self.db.get_user(telegram_id)
        
        if not user or not user.get('wallet_address'):
            await update.message.reply_text(
                "❌ No wallet registered. Use /register <wallet> first."
            )
            return
        
        wallet = user['wallet_address']
        
        # Get positions from database
        positions = self.db.get_active_positions()
        user_positions = [p for p in positions if p['wallet_address'] == wallet]
        
        if not user_positions:
            await update.message.reply_text(
                f"📊 No active positions found for:\n`{wallet[:10]}...{wallet[-8:]}`",
                parse_mode='Markdown'
            )
            return
        
        msg = f"📊 Your Positions\n\n"
        for pos in user_positions[:5]:  # Show max 5
            # Get latest snapshot
            history = self.db.get_position_history(pos['position_id'], limit=1)
            if history:
                snapshot = history[0]
                ratio = snapshot['collateral_ratio']
                
                status_emoji = "🔴" if ratio < 160 else "🟡" if ratio < 180 else "🟢"
                
                msg += f"{status_emoji} Position #{pos['position_id']}\n"
                msg += f"   Ratio: {ratio:.2f}%\n"
                msg += f"   Updated: {snapshot['snapshot_timestamp']}\n\n"
        
        if len(user_positions) > 5:
            msg += f"_...and {len(user_positions) - 5} more positions_"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def alerts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /alerts command."""
        telegram_id = str(update.effective_user.id)
        user = self.db.get_user(telegram_id)
        
        if not user:
            await update.message.reply_text("User not found.")
            return
        
        # Get recent alerts (from all positions for this user)
        # In production, filter by user's wallet
        alerts = self.db.get_unsent_alerts()
        
        if not alerts:
            await update.message.reply_text("✅ No pending alerts!")
            return
        
        msg = "🔔 Recent Alerts:\n\n"
        for alert in alerts[:5]:
            msg += f"• {alert['alert_type']}: {alert['collateral_ratio']:.2f}%\n"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def thresholds(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /thresholds command."""
        msg = f"""
⚙️ Alert Thresholds:

🟡 WARNING: < {settings.WARNING_THRESHOLD}%
🔴 CRITICAL: < {settings.CRITICAL_THRESHOLD}%
💀 LIQUIDATION: < {settings.LIQUIDATION_THRESHOLD}%

These thresholds apply to all monitored positions.
"""
        await update.message.reply_text(msg.strip())
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await self.start(update, context)
    
    async def send_alert(
        self,
        telegram_id: str,
        position_data: dict,
        ratio: float,
        alert_type: str
    ):
        """Send alert to specific user."""
        if not self.bot:
            logger.error("Bot not initialized")
            return False
        
        # Format message
        emoji = "🔴" if alert_type == "CRITICAL" else "⚠️" if alert_type == "WARNING" else "💀"
        
        message = f"""
{emoji} {alert_type} ALERT {emoji}

Wallet: `{position_data.get('wallet_address', 'Unknown')[:10]}...`
Position: #{position_data.get('position_id', 'Unknown')}
Protocol: Money on Chain

Collateral Ratio: {ratio:.2f}%
Threshold: {settings.WARNING_THRESHOLD if alert_type == 'WARNING' else settings.CRITICAL_THRESHOLD}%

Collateral: {position_data.get('collateral_rbtc', 0):.4f} RBTC (${position_data.get('collateral_usd', 0):.2f})
Debt: {position_data.get('debt_doc', 0):.2f} DOC (${position_data.get('debt_usd', 0):.2f})

Action Required: Add collateral or reduce debt

Time: {position_data.get('timestamp', 'Unknown')}
"""
        
        try:
            await self.bot.send_message(
                chat_id=telegram_id,
                text=message.strip(),
                parse_mode='Markdown'
            )
            logger.info(f"Alert sent to {telegram_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send alert to {telegram_id}: {e}")
            return False
    
    def run(self):
        """Start bot (for standalone running)."""
        if not self.token:
            logger.error("Telegram bot token not configured")
            return
        
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("register", self.register))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("alerts", self.alerts))
        self.application.add_handler(CommandHandler("thresholds", self.thresholds))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        logger.info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# Singleton instance
_bot = None

def get_bot() -> Optional[CollateralBot]:
    """Get or create CollateralBot singleton."""
    global _bot
    if _bot is None:
        if settings.TELEGRAM_BOT_TOKEN:
            _bot = CollateralBot()
        else:
            logger.warning("Telegram bot not configured (no token)")
            return None
    return _bot
