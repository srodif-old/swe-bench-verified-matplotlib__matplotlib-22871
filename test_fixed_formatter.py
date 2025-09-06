#!/usr/bin/env python3
"""
Test the actual ConciseDateFormatter with the fix applied.
"""

import sys
import os
sys.path.insert(0, '/home/runner/work/swe-bench-verified-matplotlib__matplotlib-22871/swe-bench-verified-matplotlib__matplotlib-22871/lib')

import numpy as np
from datetime import datetime, timedelta

# Import the fixed ConciseDateFormatter
try:
    from matplotlib.dates import ConciseDateFormatter
    from matplotlib.ticker import Formatter
    import matplotlib as mpl
    print("Successfully imported fixed ConciseDateFormatter")
except ImportError as e:
    print(f"Import error: {e}")
    print("Will test the logic directly")

# Mock minimal locator
class MockLocator:
    pass

def test_fixed_formatter():
    """Test that the fix works for monthly ticks."""
    
    # Monthly tick dates that would trigger the bug
    monthly_tick_dates = [
        datetime(2021, 2, 1),
        datetime(2021, 3, 1), 
        datetime(2021, 4, 1),
        datetime(2021, 5, 1),
        datetime(2021, 6, 1),
        datetime(2021, 7, 1),
        datetime(2021, 8, 1),
        datetime(2021, 9, 1),
    ]
    
    # Convert to matplotlib ordinal values (approximate)
    base_ordinal = datetime(1970, 1, 1).toordinal()
    values = [d.toordinal() - base_ordinal for d in monthly_tick_dates]
    
    print(f"Testing fixed formatter with monthly ticks:")
    print(f"Tick dates: {[d.strftime('%Y-%m-%d') for d in monthly_tick_dates]}")
    
    try:
        # Test with the actual fixed formatter
        locator = MockLocator()
        formatter = ConciseDateFormatter(locator)
        
        # Call format_ticks with our test values
        labels = formatter.format_ticks(values)
        offset = formatter.get_offset()
        
        print(f"Tick labels: {labels}")
        print(f"Offset: '{offset}'")
        
        if offset:
            print("✅ SUCCESS: Offset is now shown!")
            print(f"   Expected '2021', got '{offset}'")
            return True
        else:
            print("❌ FAIL: Offset is still hidden")
            return False
            
    except Exception as e:
        print(f"Error testing with ConciseDateFormatter: {e}")
        return False

def test_yearly_ticks_still_work():
    """Test that yearly ticks still correctly hide the offset."""
    
    # Yearly tick dates 
    yearly_tick_dates = [
        datetime(2019, 1, 1),
        datetime(2020, 1, 1), 
        datetime(2021, 1, 1),
        datetime(2022, 1, 1),
    ]
    
    # Convert to matplotlib ordinal values
    base_ordinal = datetime(1970, 1, 1).toordinal()
    values = [d.toordinal() - base_ordinal for d in yearly_tick_dates]
    
    print(f"\nTesting yearly ticks still work correctly:")
    print(f"Tick dates: {[d.strftime('%Y-%m-%d') for d in yearly_tick_dates]}")
    
    try:
        locator = MockLocator()
        formatter = ConciseDateFormatter(locator)
        
        labels = formatter.format_ticks(values)
        offset = formatter.get_offset()
        
        print(f"Tick labels: {labels}")
        print(f"Offset: '{offset}'")
        
        if not offset:
            print("✅ SUCCESS: Yearly ticks correctly hide offset")
            return True
        else:
            print("❌ UNEXPECTED: Yearly ticks are showing offset when they shouldn't")
            return False
            
    except Exception as e:
        print(f"Error testing yearly ticks: {e}")
        return False

if __name__ == "__main__":
    success1 = test_fixed_formatter()
    success2 = test_yearly_ticks_still_work()
    
    if success1 and success2:
        print("\n🎉 All tests passed! The fix works correctly.")
    else:
        print("\n❌ Some tests failed.")