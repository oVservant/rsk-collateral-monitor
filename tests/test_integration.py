#!/usr/bin/env python3
"""Integration tests for BTC Collateral Monitor."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from core.contract_reader import get_contract_reader
from core.ratio_calculator import get_ratio_calculator


def test_rsk_connection():
    """Test connection to RSK node."""
    print("🔗 Testing RSK connection...")
    
    reader = get_contract_reader()
    is_connected = reader.is_connected()
    
    assert is_connected, "Failed to connect to RSK node"
    
    block_number = reader.get_block_number()
    assert block_number > 0, "Invalid block number"
    
    print(f"✅ Connected to RSK (Block #{block_number})")
    return True


def test_contract_initialization():
    """Test contract initialization."""
    print("\n📄 Testing contract initialization...")
    
    reader = get_contract_reader()
    
    # Check if contracts are initialized
    if settings.MOC_PLATFORM_ADDRESS:
        assert reader.platform_contract is not None, "Platform contract not initialized"
        print(f"✅ MoCPlatform contract: {settings.MOC_PLATFORM_ADDRESS[:10]}...")
    else:
        print("⚠️  MoCPlatform address not configured (skipping)")
    
    if settings.DOC_TOKEN_ADDRESS:
        assert reader.doc_contract is not None, "DOC contract not initialized"
        print(f"✅ DOC token contract: {settings.DOC_TOKEN_ADDRESS[:10]}...")
    else:
        print("⚠️  DOC token address not configured (skipping)")
    
    return True


def test_ratio_calculation():
    """Test collateral ratio calculation."""
    print("\n🧮 Testing ratio calculation...")
    
    calculator = get_ratio_calculator()
    
    # Test case 1: Healthy position (200% ratio)
    # 2 RBTC collateral, 10000 DOC debt
    # Assuming RBTC = $45000, DOC = $1
    # Collateral USD = 2 * 45000 = 90000
    # Debt USD = 10000 * 1 = 10000
    # Ratio = 90000 / 10000 * 100 = 900%
    
    collateral_wei = 2 * 10**18  # 2 RBTC
    debt_wei = 10000 * 10**18    # 10000 DOC
    
    ratio = calculator.calculate_collateral_ratio(collateral_wei, debt_wei)
    print(f"   Test 1 - Healthy position: {ratio:.2f}%")
    assert ratio > 180, f"Expected >180%, got {ratio:.2f}%"
    
    # Test case 2: Warning level (170% ratio)
    # 1 RBTC collateral, 26470 DOC debt
    # Collateral USD = 1 * 45000 = 45000
    # Debt USD = 26470 * 1 = 26470
    # Ratio = 45000 / 26470 * 100 = 170%
    
    collateral_wei = 1 * 10**18
    debt_wei = 26470 * 10**18
    
    ratio = calculator.calculate_collateral_ratio(collateral_wei, debt_wei)
    print(f"   Test 2 - Warning level: {ratio:.2f}%")
    assert 160 <= ratio < 180, f"Expected 160-180%, got {ratio:.2f}%"
    
    # Test case 3: Critical level (150% ratio)
    collateral_wei = 1 * 10**18
    debt_wei = 30000 * 10**18
    
    ratio = calculator.calculate_collateral_ratio(collateral_wei, debt_wei)
    print(f"   Test 3 - Critical level: {ratio:.2f}%")
    assert ratio < 160, f"Expected <160%, got {ratio:.2f}%"
    
    # Test thresholds
    is_warning, is_critical, is_liquidation = calculator.check_thresholds(170)
    assert is_warning and not is_critical, "Warning threshold check failed"
    
    is_warning, is_critical, is_liquidation = calculator.check_thresholds(155)
    assert is_warning and is_critical and not is_liquidation, "Critical threshold check failed"
    
    print("✅ Ratio calculations correct")
    return True


def test_rbtc_price_fetch():
    """Test RBTC price fetching."""
    print("\n💰 Testing RBTC price fetch...")
    
    calculator = get_ratio_calculator()
    price = calculator.get_rbtc_price_usd()
    
    assert price > 0, "Invalid RBTC price"
    assert price < 100000, "Unreasonable RBTC price"
    
    print(f"✅ RBTC price: ${price:.2f}")
    return True


def run_all_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("BTC Collateral Monitor - Integration Tests")
    print("=" * 60)
    
    tests = [
        test_rsk_connection,
        test_contract_initialization,
        test_ratio_calculation,
        test_rbtc_price_fetch,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: Unexpected error - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
