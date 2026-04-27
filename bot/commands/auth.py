#!/usr/bin/env python3
"""Handle /verify command for wallet authentication."""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from core.auth import get_authenticator
from db.models import get_database

logger = logging.getLogger('collateral_monitor.bot.auth')


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /verify command to authenticate wallet ownership.
    
    Usage:
        /verify - Start verification process
        /verify <signature> - Complete verification
    """
    telegram_id = str(update.effective_user.id)
    db = get_database()
    authenticator = get_authenticator()
    
    # Get user from database
    user = db.get_user_by_telegram_id(telegram_id)
    
    if not user or not user.get('wallet_address'):
        await update.message.reply_text(
            "❌ You need to register a wallet first.\n\n"
            "Usage: /register <wallet_address>"
        )
        return
    
    wallet = user['wallet_address']
    
    # If no arguments, generate nonce
    if not context.args:
        nonce = authenticator.generate_nonce(telegram_id)
        message = authenticator.get_sign_message(nonce)
        
        await update.message.reply_text(
            f"🔐 **Wallet Verification**\n\n"
            f"To verify you own `{wallet[:10]}...{wallet[-8:]}`, "
            f"please sign the following message with your wallet:\n\n"
            f"`{message}`\n\n"
            f"Then send the signature with:\n"
            f"`/verify <signature>`\n\n"
            f"⏰ This request expires in 10 minutes.",
            parse_mode='Markdown'
        )
        
        logger.info(f"Started verification for {telegram_id}")
        return
    
    # Verify signature
    signature = context.args[0]
    
    if authenticator.verify_signature(telegram_id, wallet, signature):
        # Mark user as verified in database
        db.update_user_verification(telegram_id, verified=True)
        
        await update.message.reply_text(
            "✅ **Verification Successful!**\n\n"
            f"Your wallet `{wallet[:10]}...{wallet[-8:]}` has been verified.\n\n"
            f"You can now receive alerts for this wallet.",
            parse_mode='Markdown'
        )
        
        logger.info(f"Successfully verified {telegram_id}")
    else:
        await update.message.reply_text(
            "❌ **Verification Failed**\n\n"
            "The signature is invalid or expired.\n\n"
            "Please try again with /verify"
        )
        
        logger.warning(f"Verification failed for {telegram_id}")
