#!/usr/bin/env python3
"""
User authentication for multi-user support.

Uses Ethereum-style message signing to verify wallet ownership.
"""
import logging
from typing import Optional, Tuple
from web3 import Web3
from web3.eth import Account
import secrets
from datetime import datetime, timedelta

logger = logging.getLogger('collateral_monitor.auth')


class WalletAuthenticator:
    """Authenticate wallet ownership via message signing."""
    
    def __init__(self):
        self.nonces = {}  # telegram_id -> (nonce, expires_at)
        self.nonce_expiry_minutes = 10
    
    def generate_nonce(self, telegram_id: str) -> str:
        """Generate a unique nonce for authentication."""
        nonce = secrets.token_hex(16)
        expires_at = datetime.now() + timedelta(minutes=self.nonce_expiry_minutes)
        
        self.nonces[telegram_id] = (nonce, expires_at)
        
        logger.debug(f"Generated nonce for {telegram_id}: {nonce[:8]}...")
        return nonce
    
    def get_sign_message(self, nonce: str) -> str:
        """Get the message to be signed."""
        return f"Sign this message to verify wallet ownership.\n\nNonce: {nonce}\n\nThis request will expire in 10 minutes."
    
    def verify_signature(self, telegram_id: str, wallet: str, signature: str) -> bool:
        """
        Verify that the signature was signed by the wallet owner.
        
        Args:
            telegram_id: User's Telegram ID
            wallet: Wallet address to verify
            signature: Signature from wallet
        
        Returns:
            True if signature is valid and matches wallet
        """
        # Check if nonce exists and is not expired
        if telegram_id not in self.nonces:
            logger.warning(f"No nonce found for {telegram_id}")
            return False
        
        nonce, expires_at = self.nonces[telegram_id]
        
        if datetime.now() > expires_at:
            logger.warning(f"Nonce expired for {telegram_id}")
            del self.nonces[telegram_id]
            return False
        
        # Get message that was signed
        message = self.get_sign_message(nonce)
        message_hash = Web3.solidityKeccak(['string'], [message])
        
        try:
            # Recover signer from signature
            signer = Account.recoverHash(message_hash, signature=signature)
            
            # Check if signer matches wallet
            if signer.lower() == wallet.lower():
                logger.info(f"Successfully authenticated {telegram_id} with wallet {wallet[:10]}...")
                # Remove nonce after successful authentication
                del self.nonces[telegram_id]
                return True
            else:
                logger.warning(f"Signature mismatch for {telegram_id}. Expected {wallet}, got {signer}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to verify signature: {e}")
            return False
    
    def cleanup_expired_nonces(self):
        """Remove expired nonces from memory."""
        now = datetime.now()
        expired = [
            tid for tid, (_, expires_at) in self.nonces.items()
            if now > expires_at
        ]
        
        for tid in expired:
            del self.nonces[tid]
        
        if expired:
            logger.debug(f"Cleaned up {len(expired)} expired nonces")


# Singleton instance
_authenticator = None

def get_authenticator() -> WalletAuthenticator:
    """Get singleton instance of WalletAuthenticator."""
    global _authenticator
    if _authenticator is None:
        _authenticator = WalletAuthenticator()
    return _authenticator
