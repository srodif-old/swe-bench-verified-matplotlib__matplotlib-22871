#!/usr/bin/env python3
"""
Test script to reproduce the ConciseDateFormatter issue.
This test focuses on the specific case from the problem statement.
"""

import sys
import os
sys.path.insert(0, '/home/runner/work/swe-bench-verified-matplotlib__matplotlib-22871/swe-bench-verified-matplotlib__matplotlib-22871/lib')

import numpy as np
from datetime import datetime, timedelta

# Mock the minimal parts we need
class MockAutoDateLocator:
    def __call__(self):
        # Mock tick values
        return [18662.0, 18690.0, 18721.0, 18751.0, 18782.0, 18812.0, 18843.0]  # Example ticks

def num2date(value, tz=None):
    # Convert matplotlib ordinal to datetime
    base = datetime(1970, 1, 1)
    return base + timedelta(days=value)

def _wrap_in_tex(s):
    return f"${s}$"

# Mock matplotlib 
class MockMpl:
    rcParams = {'text.usetex': False, 'timezone': None}

# Now test the ConciseDateFormatter logic directly
def test_issue_case():
    """Test the specific case from the issue report."""
    
    # Simulate the original problem case: 200 days starting from 2021-02-14
    initial = datetime(2021, 2, 14, 0, 0, 0)
    time_array = [initial + timedelta(days=x) for x in range(1, 200)]
    
    # Convert to matplotlib ordinal values (approximate)
    base_ordinal = datetime(1970, 1, 1).toordinal()
    values = [d.toordinal() - base_ordinal for d in time_array]
    
    print(f"Testing date range: {time_array[0]} to {time_array[-1]}")
    print(f"Number of days: {len(time_array)}")
    
    # Test the formatter logic
    tickdatetime = time_array
    tickdate = np.array([tdt.timetuple()[:6] for tdt in tickdatetime])
    
    print(f"Years in data: {np.unique(tickdate[:, 0])}")
    print(f"Months in data: {np.unique(tickdate[:, 1])}")
    
    # Determine level (copied from actual ConciseDateFormatter)
    for level in range(5, -1, -1):
        unique_count = len(np.unique(tickdate[:, level]))
        print(f"Level {level}: {unique_count} unique values")
        if unique_count > 1:
            # This is the problematic logic
            if level < 2:
                show_offset = False
                print(f"  -> BUG: Level {level} chosen, show_offset = {show_offset} (SHOULD BE True)")
            else:
                show_offset = True
                print(f"  -> Level {level} chosen, show_offset = {show_offset}")
            break
        elif level == 0:
            level = 5
            show_offset = True
    
    # Show what the offset would be
    offset_formats = ['', '%Y', '%Y-%b', '%Y-%b-%d', '%Y-%b-%d', '%Y-%b-%d %H:%M']
    print(f"Offset format for level {level}: '{offset_formats[level]}'")
    
    if show_offset:
        offset_string = time_array[-1].strftime(offset_formats[level])
        print(f"Offset string: '{offset_string}'")
    else:
        print("Offset: (hidden) <-- THIS IS THE BUG")
    
    return level, show_offset

if __name__ == "__main__":
    test_issue_case()