#!/usr/bin/env python3
"""Unit tests for ContractReader."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from web3 import Web3

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.contract_reader import ContractReader, get_contract_reader


class TestContractReader:
    """Tests for ContractReader class."""
    
    def test_init(self):
        """Test ContractReader initialization."""
        reader = ContractReader(rpc_url='https://public-node.rsk.co')
        assert reader.rpc_url == 'https://public-node.rsk.co'
        assert reader.w3 is not None
    
    def test_is_connected_success(self):
        """Test successful connection check."""
        reader = ContractReader()
        reader.w3 = Mock()
        reader.w3.is_connected = Mock(return_value=True)
        
        assert reader.is_connected() is True
    
    def test_is_connected_failure(self):
        """Test failed connection check."""
        reader = ContractReader()
        reader.w3 = Mock()
        reader.w3.is_connected = Mock(side_effect=Exception("Connection failed"))
        
        assert reader.is_connected() is False
    
    def test_get_block_number(self):
        """Test getting block number."""
        reader = ContractReader()
        reader.w3 = Mock()
        reader.w3.eth = Mock()
        reader.w3.eth.block_number = 12345678
        
        assert reader.get_block_number() == 12345678
    
    @patch('core.contract_reader.settings')
    def test_get_positions_by_holder(self, mock_settings):
        """Test fetching positions by holder."""
        mock_settings.MOC_PLATFORM_ADDRESS = '0x1234567890123456789012345678901234567890'
        
        reader = ContractReader()
        reader.platform_contract = Mock()
        reader.platform_contract.functions.getPositionsByHolder = Mock()
        reader.platform_contract.functions.getPositionsByHolder.return_value.call = Mock(
            return_value=[1, 2, 3]
        )
        
        positions = reader.get_positions_by_holder('0x1234567890123456789012345678901234567890')
        assert positions == [1, 2, 3]
    
    def test_get_position(self):
        """Test fetching single position."""
        reader = ContractReader()
        reader.platform_contract = Mock()
        reader.platform_contract.functions.getPosition = Mock()
        
        # Mock position data: (holder, collateral, debt, timestamp)
        mock_position = (
            '0x1234567890123456789012345678901234567890',
            1000000000000000000,  # 1 RBTC in wei
            500000000000000000000,  # 500 DOC in wei
            1234567890
        )
        
        reader.platform_contract.functions.getPosition.return_value.call = Mock(
            return_value=mock_position
        )
        
        position = reader.get_position(123)
        
        assert position is not None
        assert position['position_id'] == 123
        assert position['collateral_wei'] == 1000000000000000000
        assert position['debt_wei'] == 500000000000000000000
    
    def test_get_position_not_found(self):
        """Test fetching non-existent position."""
        from web3.exceptions import ContractLogicError
        
        reader = ContractReader()
        reader.platform_contract = Mock()
        reader.platform_contract.functions.getPosition = Mock()
        reader.platform_contract.functions.getPosition.return_value.call = Mock(
            side_effect=ContractLogicError("Position not found")
        )
        
        position = reader.get_position(999)
        assert position is None


def test_singleton():
    """Test singleton pattern for get_contract_reader."""
    reader1 = get_contract_reader()
    reader2 = get_contract_reader()
    assert reader1 is reader2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
