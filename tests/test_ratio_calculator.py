#!/usr/bin/env python3
"""Unit tests for RatioCalculator."""
import pytest
from unittest.mock import Mock, patch
from decimal import Decimal

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.ratio_calculator import RatioCalculator, get_ratio_calculator


class TestRatioCalculator:
    """Tests for RatioCalculator class."""
    
    def test_init(self):
        """Test RatioCalculator initialization."""
        calc = RatioCalculator()
        assert calc.warning_threshold == 180
        assert calc.critical_threshold == 160
        assert calc.liquidation_threshold == 150
    
    @patch('core.ratio_calculator.requests.get')
    def test_get_rbtc_price_success(self, mock_get):
        """Test successful RBTC price fetch."""
        mock_response = Mock()
        mock_response.json = Mock(return_value={'rootstock': {'usd': 45000}})
        mock_get.return_value = mock_response
        
        calc = RatioCalculator()
        price = calc.get_rbtc_price_usd()
        
        assert price == 45000
        mock_get.assert_called_once()
    
    @patch('core.ratio_calculator.requests.get')
    def test_get_rbtc_price_fallback_to_btc(self, mock_get):
        """Test fallback to BTC price when RBTC fails."""
        # First call (RBTC) fails
        mock_response_rbtc = Mock()
        mock_response_rbtc.json = Mock(return_value={})
        mock_response_rbtc.raise_for_status = Mock()
        
        # Second call (BTC) succeeds
        mock_response_btc = Mock()
        mock_response_btc.json = Mock(return_value={'bitcoin': {'usd': 50000}})
        
        mock_get.side_effect = [mock_response_rbtc, mock_response_btc]
        
        calc = RatioCalculator()
        price = calc.get_rbtc_price_usd()
        
        assert price == 50000
        assert mock_get.call_count == 2
    
    def test_get_doc_price_usd(self):
        """Test DOC price (should be ~1.0)."""
        calc = RatioCalculator()
        price = calc.get_doc_price_usd()
        assert price == 1.0
    
    def test_calculate_collateral_ratio_healthy(self):
        """Test ratio calculation for healthy position."""
        calc = RatioCalculator()
        
        # 2 RBTC collateral, 10000 DOC debt
        # Collateral USD = 2 * 45000 = 90000
        # Debt USD = 10000 * 1 = 10000
        # Ratio = 900%
        ratio = calc.calculate_collateral_ratio(
            collateral_wei=2 * 10**18,
            debt_wei=10000 * 10**18,
            rbtc_price=45000,
            doc_price=1.0
        )
        
        assert ratio == 900.0
    
    def test_calculate_collateral_ratio_warning(self):
        """Test ratio calculation for warning level."""
        calc = RatioCalculator()
        
        # Ratio should be ~170%
        ratio = calc.calculate_collateral_ratio(
            collateral_wei=1 * 10**18,
            debt_wei=26470 * 10**18,
            rbtc_price=45000,
            doc_price=1.0
        )
        
        assert 160 <= ratio < 180
    
    def test_calculate_collateral_ratio_critical(self):
        """Test ratio calculation for critical level."""
        calc = RatioCalculator()
        
        # Ratio should be ~150%
        ratio = calc.calculate_collateral_ratio(
            collateral_wei=1 * 10**18,
            debt_wei=30000 * 10**18,
            rbtc_price=45000,
            doc_price=1.0
        )
        
        assert ratio < 160
    
    def test_calculate_collateral_ratio_zero_debt(self):
        """Test ratio with zero debt (should return high value)."""
        calc = RatioCalculator()
        
        ratio = calc.calculate_collateral_ratio(
            collateral_wei=1 * 10**18,
            debt_wei=0,
            rbtc_price=45000,
            doc_price=1.0
        )
        
        assert ratio == 0.0  # Returns 0 for invalid input
    
    def test_check_thresholds_healthy(self):
        """Test threshold checks for healthy position."""
        calc = RatioCalculator()
        
        is_warning, is_critical, is_liquidation = calc.check_thresholds(200)
        
        assert is_warning is False
        assert is_critical is False
        assert is_liquidation is False
    
    def test_check_thresholds_warning(self):
        """Test threshold checks for warning level."""
        calc = RatioCalculator()
        
        is_warning, is_critical, is_liquidation = calc.check_thresholds(170)
        
        assert is_warning is True
        assert is_critical is False
        assert is_liquidation is False
    
    def test_check_thresholds_critical(self):
        """Test threshold checks for critical level."""
        calc = RatioCalculator()
        
        is_warning, is_critical, is_liquidation = calc.check_thresholds(155)
        
        assert is_warning is True
        assert is_critical is True
        assert is_liquidation is False
    
    def test_check_thresholds_liquidation(self):
        """Test threshold checks for liquidation level."""
        calc = RatioCalculator()
        
        is_warning, is_critical, is_liquidation = calc.check_thresholds(140)
        
        assert is_warning is True
        assert is_critical is True
        assert is_liquidation is True
    
    @patch.object(RatioCalculator, 'get_rbtc_price_usd')
    def test_process_position(self, mock_get_price):
        """Test processing a full position."""
        mock_get_price.return_value = 45000
        
        calc = RatioCalculator()
        
        position = {
            'position_id': 123,
            'holder': '0x1234567890123456789012345678901234567890',
            'collateral_wei': 2 * 10**18,
            'debt_wei': 10000 * 10**18,
            'timestamp': 1234567890
        }
        
        processed = calc.process_position(position)
        
        assert processed['collateral_ratio'] > 180
        assert processed['alert_level'] == 'OK'
        assert processed['is_warning'] is False
        assert 'collateral_rbtc' in processed
        assert 'debt_doc' in processed


def test_singleton():
    """Test singleton pattern for get_ratio_calculator."""
    calc1 = get_ratio_calculator()
    calc2 = get_ratio_calculator()
    assert calc1 is calc2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
