"""Money on Chain contract reader for RSK blockchain."""
import logging
from typing import Dict, List, Optional
from web3 import Web3
from web3.exceptions import ContractLogicError

from config.settings import settings

logger = logging.getLogger('collateral_monitor.contract_reader')

# Minimal ABI for MoCPlatform contract
MOC_PLATFORM_ABI = [
    {
        "inputs": [{"name": "holder", "type": "address"}],
        "name": "getAmountOfPos",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "positionId", "type": "uint256"}],
        "name": "getPosition",
        "outputs": [
            {"name": "holder", "type": "address"},
            {"name": "collateral", "type": "uint256"},
            {"name": "debt", "type": "uint256"},
            {"name": "timestamp", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "holder", "type": "address"}],
        "name": "getPositionsByHolder",
        "outputs": [{"name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ERC20 ABI for DOC token
ERC20_ABI = [
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]


class ContractReader:
    """Reads data from Money on Chain contracts on RSK."""
    
    def __init__(self, rpc_url: str = None):
        """Initialize Web3 connection."""
        self.rpc_url = rpc_url or settings.RSK_RPC_URL
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Initialize contracts
        if settings.MOC_PLATFORM_ADDRESS:
            self.platform_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(settings.MOC_PLATFORM_ADDRESS),
                abi=MOC_PLATFORM_ABI
            )
            logger.info(f"MoCPlatform contract initialized: {settings.MOC_PLATFORM_ADDRESS}")
        else:
            self.platform_contract = None
            logger.warning("MoCPlatform address not configured")
        
        if settings.DOC_TOKEN_ADDRESS:
            self.doc_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(settings.DOC_TOKEN_ADDRESS),
                abi=ERC20_ABI
            )
            logger.info(f"DOC token contract initialized: {settings.DOC_TOKEN_ADDRESS}")
        else:
            self.doc_contract = None
    
    def is_connected(self) -> bool:
        """Check if connected to RSK node."""
        try:
            return self.w3.is_connected()
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False
    
    def get_block_number(self) -> int:
        """Get current block number."""
        return self.w3.eth.block_number
    
    def get_positions_by_holder(self, holder_address: str) -> List[int]:
        """Get all position IDs for a wallet address."""
        if not self.platform_contract:
            raise ValueError("Platform contract not initialized")
        
        try:
            checksum_addr = Web3.to_checksum_address(holder_address)
            position_ids = self.platform_contract.functions.getPositionsByHolder(
                checksum_addr
            ).call()
            
            logger.info(f"Found {len(position_ids)} positions for {holder_address[:8]}...")
            return position_ids
            
        except ContractLogicError as e:
            logger.error(f"Contract call failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []
    
    def get_position(self, position_id: int) -> Optional[Dict]:
        """Get details for a specific position."""
        if not self.platform_contract:
            raise ValueError("Platform contract not initialized")
        
        try:
            position = self.platform_contract.functions.getPosition(position_id).call()
            
            return {
                'position_id': position_id,
                'holder': position[0],
                'collateral_wei': position[1],
                'debt_wei': position[2],
                'timestamp': position[3]
            }
            
        except ContractLogicError as e:
            logger.error(f"Position {position_id} not found: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching position {position_id}: {e}")
            return None
    
    def get_all_positions(self, wallet_addresses: List[str]) -> List[Dict]:
        """Fetch all positions for multiple wallets."""
        all_positions = []
        
        for wallet in wallet_addresses:
            try:
                position_ids = self.get_positions_by_holder(wallet)
                
                for pos_id in position_ids:
                    position_data = self.get_position(pos_id)
                    if position_data:
                        position_data['wallet_address'] = wallet
                        all_positions.append(position_data)
                
            except Exception as e:
                logger.error(f"Error processing wallet {wallet}: {e}")
                continue
        
        logger.info(f"Fetched {len(all_positions)} total positions")
        return all_positions
    
    def get_doc_balance(self, address: str) -> int:
        """Get DOC token balance for an address."""
        if not self.doc_contract:
            raise ValueError("DOC contract not initialized")
        
        try:
            checksum_addr = Web3.to_checksum_address(address)
            balance = self.doc_contract.functions.balanceOf(checksum_addr).call()
            return balance
        except Exception as e:
            logger.error(f"Error fetching DOC balance: {e}")
            return 0


# Singleton instance
_contract_reader = None

def get_contract_reader() -> ContractReader:
    """Get or create ContractReader singleton."""
    global _contract_reader
    if _contract_reader is None:
        _contract_reader = ContractReader()
    return _contract_reader
