#!/usr/bin/env python3
"""
Test what happens when AutoDateLocator chooses monthly ticks.
This might be the actual scenario that triggers the bug.
"""

import sys
import os
sys.path.insert(0, '/home/runner/work/swe-bench-verified-matplotlib__matplotlib-22871/swe-bench-verified-matplotlib__matplotlib-22871/lib')

import numpy as np
from datetime import datetime, timedelta

def test_monthly_ticks_scenario():
    """Test when ticks are placed at month boundaries."""
    
    # Let's say AutoDateLocator chooses to place ticks at the beginning of each month
    # for the 200-day span from Feb 2021 to Sep 2021
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
    
    print(f"Testing monthly ticks scenario:")
    print(f"Tick dates: {[d.strftime('%Y-%m-%d') for d in monthly_tick_dates]}")
    
    # Test the formatter logic with these monthly ticks
    tickdatetime = monthly_tick_dates
    tickdate = np.array([tdt.timetuple()[:6] for tdt in tickdatetime])
    
    print(f"Years in ticks: {np.unique(tickdate[:, 0])}")
    print(f"Months in ticks: {np.unique(tickdate[:, 1])}")
    print(f"Days in ticks: {np.unique(tickdate[:, 2])}")
    
    # Determine level (copied from actual ConciseDateFormatter)
    show_offset = True  # default
    for level in range(5, -1, -1):
        unique_count = len(np.unique(tickdate[:, level]))
        print(f"Level {level}: {unique_count} unique values")
        if unique_count > 1:
            # This is the problematic logic
            if level < 2:
                show_offset = False
                print(f"  -> BUG TRIGGERED: Level {level} chosen, show_offset = {show_offset}")
                print(f"     This means level is {'years' if level == 0 else 'months'}, so offset is hidden!")
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
        offset_string = monthly_tick_dates[-1].strftime(offset_formats[level])
        print(f"Offset string: '{offset_string}'")
    else:
        print("Offset: (hidden) <-- THIS IS THE BUG!")
        print("User expects to see '2021' but it's hidden!")
    
    return level, show_offset

def test_yearly_ticks_scenario():
    """Test when ticks span multiple years."""
    
    # Multi-year scenario
    yearly_tick_dates = [
        datetime(2019, 1, 1),
        datetime(2020, 1, 1), 
        datetime(2021, 1, 1),
        datetime(2022, 1, 1),
    ]
    
    print(f"\nTesting yearly ticks scenario:")
    print(f"Tick dates: {[d.strftime('%Y-%m-%d') for d in yearly_tick_dates]}")
    
    # Test the formatter logic with these yearly ticks
    tickdatetime = yearly_tick_dates
    tickdate = np.array([tdt.timetuple()[:6] for tdt in tickdatetime])
    
    print(f"Years in ticks: {np.unique(tickdate[:, 0])}")
    print(f"Months in ticks: {np.unique(tickdate[:, 1])}")
    
    # Determine level
    show_offset = True  # default
    for level in range(5, -1, -1):
        unique_count = len(np.unique(tickdate[:, level]))
        print(f"Level {level}: {unique_count} unique values")
        if unique_count > 1:
            if level < 2:
                show_offset = False
                print(f"  -> Level {level} chosen, show_offset = {show_offset}")
                print(f"     This makes sense for yearly ticks - no need for year in offset")
            else:
                show_offset = True
                print(f"  -> Level {level} chosen, show_offset = {show_offset}")
            break
        elif level == 0:
            level = 5
            show_offset = True
    
    offset_formats = ['', '%Y', '%Y-%b', '%Y-%b-%d', '%Y-%b-%d', '%Y-%b-%d %H:%M']
    if show_offset:
        offset_string = yearly_tick_dates[-1].strftime(offset_formats[level])
        print(f"Offset string: '{offset_string}'")
    else:
        print("Offset: (hidden) - This is reasonable for yearly ticks")

if __name__ == "__main__":
    level1, show1 = test_monthly_ticks_scenario()
    test_yearly_ticks_scenario()
    
    print(f"\n=== CONCLUSION ===")
    if level1 == 1 and not show1:
        print("BUG CONFIRMED: Monthly ticks hide the year offset!")
        print("Solution: Modify the condition to show offset for monthly ticks when useful")
    else:
        print("This scenario doesn't trigger the bug.")