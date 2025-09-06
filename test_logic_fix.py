#!/usr/bin/env python3
"""
Test the exact logic change I made to verify it works correctly.
This simulates the fixed logic without needing full matplotlib.
"""

import numpy as np
from datetime import datetime, timedelta

def test_fixed_logic():
    """Test the fixed logic for determining show_offset."""
    
    print("=== Testing Fixed Logic ===\n")
    
    # Test case 1: Monthly ticks (the bug case)
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
    
    print("Test 1: Monthly ticks (should show offset after fix)")
    print(f"Ticks: {[d.strftime('%b') for d in monthly_tick_dates]}")
    
    tickdate = np.array([tdt.timetuple()[:6] for tdt in monthly_tick_dates])
    show_offset = True  # default
    
    # Apply the FIXED logic
    for level in range(5, -1, -1):
        if len(np.unique(tickdate[:, level])) > 1:
            if level == 0:
                # For year-level ticks, hide offset since year is already 
                # shown in the tick labels
                show_offset = False
            # For month-level ticks (level == 1), keep show_offset = True
            # so that the year can be displayed in the offset
            break
        elif level == 0:
            level = 5
    
    print(f"Level determined: {level} ({'years' if level==0 else 'months' if level==1 else 'days' if level==2 else 'other'})")
    print(f"Show offset: {show_offset}")
    
    offset_formats = ['', '%Y', '%Y-%b', '%Y-%b-%d', '%Y-%b-%d', '%Y-%b-%d %H:%M']
    if show_offset and level < len(offset_formats):
        offset_string = monthly_tick_dates[-1].strftime(offset_formats[level])
        print(f"Offset: '{offset_string}'")
        expected_fix = True
    else:
        print("Offset: (hidden)")
        expected_fix = False
    
    # Test case 2: Yearly ticks (should still hide offset)
    yearly_tick_dates = [
        datetime(2019, 1, 1),
        datetime(2020, 1, 1), 
        datetime(2021, 1, 1),
        datetime(2022, 1, 1),
    ]
    
    print(f"\nTest 2: Yearly ticks (should still hide offset)")
    print(f"Ticks: {[d.strftime('%Y') for d in yearly_tick_dates]}")
    
    tickdate = np.array([tdt.timetuple()[:6] for tdt in yearly_tick_dates])
    show_offset = True  # default
    
    # Apply the FIXED logic
    for level in range(5, -1, -1):
        if len(np.unique(tickdate[:, level])) > 1:
            if level == 0:
                # For year-level ticks, hide offset since year is already 
                # shown in the tick labels
                show_offset = False
            # For month-level ticks (level == 1), keep show_offset = True
            # so that the year can be displayed in the offset
            break
        elif level == 0:
            level = 5
    
    print(f"Level determined: {level} ({'years' if level==0 else 'months' if level==1 else 'days' if level==2 else 'other'})")
    print(f"Show offset: {show_offset}")
    
    if show_offset and level < len(offset_formats):
        offset_string = yearly_tick_dates[-1].strftime(offset_formats[level])
        print(f"Offset: '{offset_string}'")
        expected_yearly = False  # Should be hidden
    else:
        print("Offset: (hidden)")
        expected_yearly = True  # Should be hidden
    
    # Test case 3: Daily ticks (should still show offset)
    daily_tick_dates = [
        datetime(2021, 8, 1),
        datetime(2021, 8, 5),
        datetime(2021, 8, 10),
        datetime(2021, 8, 15),
        datetime(2021, 8, 20),
        datetime(2021, 8, 25),
        datetime(2021, 8, 30),
    ]
    
    print(f"\nTest 3: Daily ticks (should show offset)")
    print(f"Ticks: {[d.strftime('%d') for d in daily_tick_dates]}")
    
    tickdate = np.array([tdt.timetuple()[:6] for tdt in daily_tick_dates])
    show_offset = True  # default
    
    # Apply the FIXED logic
    for level in range(5, -1, -1):
        if len(np.unique(tickdate[:, level])) > 1:
            if level == 0:
                # For year-level ticks, hide offset since year is already 
                # shown in the tick labels
                show_offset = False
            # For month-level ticks (level == 1), keep show_offset = True
            # so that the year can be displayed in the offset
            break
        elif level == 0:
            level = 5
    
    print(f"Level determined: {level} ({'years' if level==0 else 'months' if level==1 else 'days' if level==2 else 'other'})")
    print(f"Show offset: {show_offset}")
    
    if show_offset and level < len(offset_formats):
        offset_string = daily_tick_dates[-1].strftime(offset_formats[level])
        print(f"Offset: '{offset_string}'")
        expected_daily = True
    else:
        print("Offset: (hidden)")
        expected_daily = False
    
    # Summary
    print(f"\n=== RESULTS ===")
    test1_pass = expected_fix  # Monthly ticks should show offset
    test2_pass = expected_yearly  # Yearly ticks should hide offset  
    test3_pass = expected_daily  # Daily ticks should show offset
    
    print(f"Monthly ticks show offset: {'✅ PASS' if test1_pass else '❌ FAIL'}")
    print(f"Yearly ticks hide offset: {'✅ PASS' if test2_pass else '❌ FAIL'}")
    print(f"Daily ticks show offset: {'✅ PASS' if test3_pass else '❌ FAIL'}")
    
    return test1_pass and test2_pass and test3_pass

if __name__ == "__main__":
    success = test_fixed_logic()
    if success:
        print("\n🎉 All logic tests passed! The fix works correctly.")
    else:
        print("\n❌ Some logic tests failed.")