# Development Guide

This guide is for developers who want to contribute to BTC Collateral Monitor.

## Table of Contents

- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Debugging](#debugging)
- [Building](#building)
- [Releasing](#releasing)

## Development Setup

### Prerequisites

- Python 3.10+
- pip and virtualenv
- Git
- Docker (optional, for container testing)

### Quick Start

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/rsk-collateral-monitor.git
cd rsk-collateral-monitor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Copy environment file
cp .env.example .env

# Run tests
python tests/test_integration.py
```

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
# Install
pre-commit install

# Run manually
pre-commit run --all-files
```

Hooks include:
- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- trailing-whitespace
- end-of-file-fixer
- detect-private-key

## Code Style

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://pycqa.github.io/isort/) for imports
- Maximum line length: 100 characters
- Use type hints for function signatures

### Example

```python
from typing import Dict, List, Optional
from web3 import Web3

def calculate_ratio(collateral_wei: int, debt_wei: int) -> float:
    """Calculate collateral ratio percentage.
    
    Args:
        collateral_wei: Collateral amount in wei
        debt_wei: Debt amount in wei
    
    Returns:
        Collateral ratio as percentage
    
    Raises:
        ValueError: If debt_wei is zero or negative
    """
    if debt_wei <= 0:
        raise ValueError("Debt must be positive")
    
    ratio = (collateral_wei / debt_wei) * 100
    return round(ratio, 2)
```

### Type Hints

Use type hints for all function parameters and return values:

```python
from typing import Dict, List, Optional, Tuple

def fetch_positions(wallet: str) -> List[Dict]:
    ...

def check_thresholds(ratio: float) -> Tuple[bool, bool, bool]:
    ...
```

## Testing

### Running Tests

```bash
# Run all tests
python tests/test_integration.py

# Run with pytest (if installed)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Writing Tests

Tests should:
- Be named `test_*.py`
- Use descriptive test function names
- Test one thing per function
- Include both happy path and edge cases

Example:

```python
def test_ratio_calculation_healthy_position():
    """Test ratio calculation for healthy position (>180%)."""
    calculator = RatioCalculator()
    ratio = calculator.calculate_collateral_ratio(
        collateral_wei=2 * 10**18,
        debt_wei=10000 * 10**18
    )
    assert ratio > 180
```

### Integration Tests

Integration tests require:
- RSK node connection
- Environment variables configured

Make sure `.env` file is properly configured before running.

## Debugging

### Logging

The project uses Python logging module:

```python
import logging

logger = logging.getLogger('collateral_monitor.module_name')

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debug Mode

Set log level to DEBUG in `.env`:

```bash
LOG_LEVEL=DEBUG
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

---

**Last Updated:** 2026-04-27
