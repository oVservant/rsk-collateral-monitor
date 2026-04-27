"""Collateral ratio calculator for BTC positions."""
import logging
from typing import Dict, Tuple
from decimal import Decimal
import requests

from config.settings import settings

logger = logging.getLogger('collateral_monitor.ratio_calculator')


class RatioCalculator:
    """Calculates collateral ratios and checks thresholds."""
    
    def __init__(self):
        self.warning_threshold = settings.WARNING_THRESHOLD
        self.critical_threshold = settings.CRITICAL_THRESHOLD
        self.liquidation_threshold = settings.LIQUIDATION_THRESHOLD
    
    def get_rbtc_price_usd(self) -> float:
        """Fetch current RBTC price in USD."""
        try:
            # Try CoinGecko API (free, no auth required)
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={'ids': 'rootstock', 'vs_currencies': 'usd'},
                timeout=5
            )
            data = response.json()
            price = data.get('rootstock', {}).get('usd', 0)
            
            if price > 0:
                logger.info(f"RBTC price: ${price:.2f}")
                return price
            
            # Fallback: use BTC price as approximation
            logger.warning("CoinGecko RBTC price failed, using BTC as fallback")
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={'ids': 'bitcoin', 'vs_currencies': 'usd'},
                timeout=5
            )
            data = response.json()
            return data.get('bitcoin', {}).get('usd', 45000)  # Default fallback
            
        except Exception as e:
            logger.error(f"Error fetching RBTC price: {e}")
            return 45000  # Safe default
    
    def get_doc_price_usd(self) -> float:
        """Fetch current DOC price in USD (should be ~1.0)."""
        # DOC is USD-pegged stablecoin, assume 1.0
        # In production, fetch from DEX or oracle
        return 1.0
    
    def calculate_collateral_ratio(
        self,
        collateral_wei: int,
        debt_wei: int,
        rbtc_price: float = None,
        doc_price: float = None
    ) -> float:
        """
        Calculate collateral ratio percentage.
        
        Formula:
            collateral_value_usd = (collateral_wei / 1e18) * rbtc_price
            debt_value_usd = (debt_wei / 1e18) * doc_price
            ratio = (collateral_value_usd / debt_value_usd) * 100
        
        Args:
            collateral_wei: Collateral amount in wei (RBTC, 18 decimals)
            debt_wei: Debt amount in wei (DOC, 18 decimals)
            rbtc_price: RBTC price in USD (fetches if None)
            doc_price: DOC price in USD (default 1.0)
        
        Returns:
            Collateral ratio as percentage (e.g., 175.50)
        """
        if collateral_wei <= 0 or debt_wei <= 0:
            logger.warning(f"Invalid amounts: collateral={collateral_wei}, debt={debt_wei}")
            return 0.0
        
        if rbtc_price is None:
            rbtc_price = self.get_rbtc_price_usd()
        
        if doc_price is None:
            doc_price = self.get_doc_price_usd()
        
        # Convert wei to tokens (18 decimals)
        collateral_tokens = Decimal(collateral_wei) / Decimal(10**18)
        debt_tokens = Decimal(debt_wei) / Decimal(10**18)
        
        # Calculate USD values
        collateral_usd = float(collateral_tokens) * rbtc_price
        debt_usd = float(debt_tokens) * doc_price
        
        if debt_usd <= 0:
            logger.warning("Debt USD value is zero or negative")
            return 999.99  # Effectively infinite ratio
        
        # Calculate ratio
        ratio = (collateral_usd / debt_usd) * 100
        
        logger.debug(
            f"Ratio calculation: {collateral_tokens:.4f} RBTC (${collateral_usd:.2f}) / "
            f"{debt_tokens:.2f} DOC (${debt_usd:.2f}) = {ratio:.2f}%"
        )
        
        return round(ratio, 2)
    
    def check_thresholds(self, ratio: float) -> Tuple[bool, bool, bool]:
        """
        Check if ratio breaches thresholds.
        
        Returns:
            (is_warning, is_critical, is_liquidation) tuple
        """
        is_warning = ratio < self.warning_threshold
        is_critical = ratio < self.critical_threshold
        is_liquidation = ratio < self.liquidation_threshold
        
        if is_liquidation:
            logger.warning(f"LIQUIDATION RISK: Ratio {ratio:.2f}% < {self.liquidation_threshold}%")
        elif is_critical:
            logger.warning(f"CRITICAL: Ratio {ratio:.2f}% < {self.critical_threshold}%")
        elif is_warning:
            logger.info(f"WARNING: Ratio {ratio:.2f}% < {self.warning_threshold}%")
        
        return is_warning, is_critical, is_liquidation
    
    def process_position(self, position: Dict) -> Dict:
        """
        Process a position and calculate all metrics.
        
        Args:
            position: Dict with position data from ContractReader
        
        Returns:
            Enhanced position dict with ratios and alerts
        """
        collateral_wei = position.get('collateral_wei', 0)
        debt_wei = position.get('debt_wei', 0)
        
        # Get prices
        rbtc_price = self.get_rbtc_price_usd()
        doc_price = self.get_doc_price_usd()
        
        # Calculate ratio
        ratio = self.calculate_collateral_ratio(
            collateral_wei, debt_wei, rbtc_price, doc_price
        )
        
        # Check thresholds
        is_warning, is_critical, is_liquidation = self.check_thresholds(ratio)
        
        # Convert to human-readable format
        collateral_rbtc = Decimal(collateral_wei) / Decimal(10**18)
        debt_doc = Decimal(debt_wei) / Decimal(10**18)
        
        return {
            **position,
            'collateral_rbtc': float(collateral_rbtc),
            'debt_doc': float(debt_doc),
            'collateral_usd': float(collateral_rbtc) * rbtc_price,
            'debt_usd': float(debt_doc) * doc_price,
            'collateral_ratio': ratio,
            'rbtc_price_usd': rbtc_price,
            'doc_price_usd': doc_price,
            'is_warning': is_warning,
            'is_critical': is_critical,
            'is_liquidation': is_liquidation,
            'alert_level': 'LIQUIDATION' if is_liquidation else 'CRITICAL' if is_critical else 'WARNING' if is_warning else 'OK'
        }


# Singleton instance
_ratio_calculator = None

def get_ratio_calculator() -> RatioCalculator:
    """Get or create RatioCalculator singleton."""
    global _ratio_calculator
    if _ratio_calculator is None:
        _ratio_calculator = RatioCalculator()
    return _ratio_calculator
