import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

def assertround(actual, expected, decimal_places=2):
    """
    Assert that two values are equal when rounded to the specified number of decimal places.
    
    Args:
        actual: The actual value to test
        expected: The expected value
        decimal_places: Number of decimal places to round to (default: 2)
    """
    assert round(actual, decimal_places) == round(expected, decimal_places), \
        f"Expected {expected} but got {actual} (rounded to {decimal_places} decimal places)"
