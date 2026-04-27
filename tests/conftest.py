#!/usr/bin/env python3
"""Pytest configuration and fixtures."""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_position():
    """Sample position data for testing."""
    return {
        'position_id': 123,
        'holder': '0x1234567890123456789012345678901234567890',
        'collateral_wei': 2 * 10**18,  # 2 RBTC
        'debt_wei': 10000 * 10**18,    # 10000 DOC
        'timestamp': 1234567890
    }


@pytest.fixture
def sample_wallet():
    """Sample wallet address for testing."""
    return '0x1234567890123456789012345678901234567890'


@pytest.fixture
def mock_prices():
    """Mock price data."""
    return {
        'rbtc_usd': 45000,
        'doc_usd': 1.0
    }


@pytest.fixture
def thresholds():
    """Alert thresholds."""
    return {
        'warning': 180,
        'critical': 160,
        'liquidation': 150
    }
