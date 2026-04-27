"""Configuration loader for BTC Collateral Monitor."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

class Settings:
    # RSK Configuration
    RSK_RPC_URL = os.getenv('RSK_RPC_URL', 'https://public-node.rsk.co')
    RSK_CHAIN_ID = int(os.getenv('RSK_CHAIN_ID', '30'))
    
    # Money on Chain Contracts
    MOC_PLATFORM_ADDRESS = os.getenv('MOC_PLATFORM_ADDRESS')
    MOC_HOLDER_ADDRESS = os.getenv('MOC_HOLDER_ADDRESS')
    DOC_TOKEN_ADDRESS = os.getenv('DOC_TOKEN_ADDRESS')
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_ADMIN_ID = os.getenv('TELEGRAM_ADMIN_ID')
    
    # Alert Thresholds
    WARNING_THRESHOLD = float(os.getenv('WARNING_THRESHOLD', '180'))
    CRITICAL_THRESHOLD = float(os.getenv('CRITICAL_THRESHOLD', '160'))
    LIQUIDATION_THRESHOLD = float(os.getenv('LIQUIDATION_THRESHOLD', '150'))
    
    # Polling
    POLL_INTERVAL_MINUTES = int(os.getenv('POLL_INTERVAL_MINUTES', '10'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '50'))
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/collateral_monitor.db')
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        required = ['MOC_PLATFORM_ADDRESS', 'TELEGRAM_BOT_TOKEN']
        missing = [attr for attr in required if not getattr(cls, attr)]
        
        if missing:
            raise ValueError(f"Missing required config: {missing}")
        
        return True

settings = Settings()
