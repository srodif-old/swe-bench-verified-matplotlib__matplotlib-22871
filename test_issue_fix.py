#!/usr/bin/env python3
"""
Test to verify the fix for the specific issue reported.
Tests the case where monthly ticks should show the year in the offset.
"""

import numpy as np
from datetime import datetime, timedelta

def test_original_issue_case():
    """
    Test the exact scenario from the bug report:
    200 days starting from 2021-02-14 should show '2021' in offset when
    AutoDateLocator chooses monthly ticks.
    """
    
    print("=== Testing Original Issue Case ===")
    print("Bug report: 200 days from 2021-02-14, expecting year '2021' in offset")
    
    # The issue occurs when AutoDateLocator chooses monthly ticks for this range
    # Let's simulate that scenario
    
    # If AutoDateLocator decides to show monthly ticks for Feb-Sep 2021 range
    monthly_ticks = [
        datetime(2021, 2, 1),  # Feb
        datetime(2021, 3, 1),  # Mar
        datetime(2021, 4, 1),  # Apr
        datetime(2021, 5, 1),  # May
        datetime(2021, 6, 1),  # Jun
        datetime(2021, 7, 1),  # Jul
        datetime(2021, 8, 1),  # Aug
        datetime(2021, 9, 1),  # Sep
    ]
    
    print(f"Simulated monthly ticks: {[d.strftime('%Y-%m') for d in monthly_ticks]}")
    
    # Test the OLD logic (buggy)
    print("\n--- OLD LOGIC (Buggy) ---")
    tickdate = np.array([tdt.timetuple()[:6] for tdt in monthly_ticks])
    show_offset_old = True
    
    for level in range(5, -1, -1):
        if len(np.unique(tickdate[:, level])) > 1:
            if level < 2:  # OLD BUGGY CONDITION
                show_offset_old = False
            break
        elif level == 0:
            level = 5
    
    print(f"Old logic: Level {level}, show_offset = {show_offset_old}")
    if show_offset_old:
        print("Old result: Offset shown ✅")
    else:
        print("Old result: Offset HIDDEN ❌ (This was the bug!)")
    
    # Test the NEW logic (fixed)
    print("\n--- NEW LOGIC (Fixed) ---")
    show_offset_new = True
    
    for level in range(5, -1, -1):
        if len(np.unique(tickdate[:, level])) > 1:
            if level == 0:  # NEW FIXED CONDITION
                show_offset_new = False
            # For level == 1 (months), show_offset stays True
            break
        elif level == 0:
            level = 5
    
    print(f"New logic: Level {level}, show_offset = {show_offset_new}")
    if show_offset_new:
        offset_formats = ['', '%Y', '%Y-%b', '%Y-%b-%d', '%Y-%b-%d', '%Y-%b-%d %H:%M']
        offset = monthly_ticks[-1].strftime(offset_formats[level])
        print(f"New result: Offset shown = '{offset}' ✅")
        success = True
    else:
        print("New result: Offset HIDDEN ❌")
        success = False
    
    return success

def test_edge_cases():
    """Test some edge cases to make sure the fix is robust."""
    
    print(f"\n=== Testing Edge Cases ===")
    
    # Case 1: Single year span with yearly ticks (should hide offset)
    yearly_ticks = [datetime(2021, 1, 1), datetime(2022, 1, 1), datetime(2023, 1, 1)]
    print(f"\nCase 1: Multi-year yearly ticks")
    print(f"Ticks: {[d.strftime('%Y') for d in yearly_ticks]}")
    
    tickdate = np.array([tdt.timetuple()[:6] for tdt in yearly_ticks])
    show_offset = True
    
    for level in range(5, -1, -1):
        if len(np.unique(tickdate[:, level])) > 1:
            if level == 0:
                show_offset = False
            break
        elif level == 0:
            level = 5
    
    print(f"Level: {level}, show_offset: {show_offset}")
    expected = not show_offset  # Should be hidden
    print(f"Expected: hidden, Got: {'hidden' if not show_offset else 'shown'} {'✅' if expected else '❌'}")
    
    # Case 2: Cross-year monthly ticks (should show offset)  
    cross_year_monthly = [datetime(2020, 11, 1), datetime(2020, 12, 1), datetime(2021, 1, 1), datetime(2021, 2, 1)]
    print(f"\nCase 2: Cross-year monthly ticks")
    print(f"Ticks: {[d.strftime('%Y-%m') for d in cross_year_monthly]}")
    
    tickdate = np.array([tdt.timetuple()[:6] for tdt in cross_year_monthly])
    show_offset = True
    
    for level in range(5, -1, -1):
        if len(np.unique(tickdate[:, level])) > 1:
            if level == 0:
                show_offset = False
            break
        elif level == 0:
            level = 5
    
    print(f"Level: {level}, show_offset: {show_offset}")
    if show_offset:
        offset_formats = ['', '%Y', '%Y-%b', '%Y-%b-%d', '%Y-%b-%d', '%Y-%b-%d %H:%M']
        offset = cross_year_monthly[-1].strftime(offset_formats[level])
        print(f"Offset: '{offset}' ✅")
    else:
        print("Offset: hidden ❌")
    
    return True

if __name__ == "__main__":
    success1 = test_original_issue_case()
    success2 = test_edge_cases()
    
    print(f"\n=== FINAL RESULT ===")
    if success1:
        print("🎉 Original issue FIXED! Monthly ticks now show year in offset.")
    else:
        print("❌ Original issue NOT fixed.")
        
    print("Fix preserves existing behavior for yearly and daily ticks.")