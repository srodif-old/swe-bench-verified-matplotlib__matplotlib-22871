#!/usr/bin/env python3

# Test to understand when the issue occurs
import numpy as np
from datetime import datetime, timedelta

def test_date_range(start_date, num_days, desc):
    print(f"\n=== Testing {desc} ===")
    test_dates = [start_date + timedelta(days=x) for x in range(num_days)]
    tickdate = np.array([tdt.timetuple()[:6] for tdt in test_dates])
    
    print(f"Date range: {test_dates[0].strftime('%Y-%m-%d')} to {test_dates[-1].strftime('%Y-%m-%d')}")
    print(f"Years: {len(np.unique(tickdate[:, 0]))} unique -> {np.unique(tickdate[:, 0])}")
    print(f"Months: {len(np.unique(tickdate[:, 1]))} unique -> {np.unique(tickdate[:, 1])}")
    print(f"Days: {len(np.unique(tickdate[:, 2]))} unique -> range {np.min(tickdate[:, 2])}-{np.max(tickdate[:, 2])}")
    
    # Find the level
    for level in range(5, -1, -1):
        unique_count = len(np.unique(tickdate[:, level]))
        if unique_count > 1:
            if level < 2:
                show_offset = False
            else:
                show_offset = True
            print(f"Level determined: {level} ({'years' if level==0 else 'months' if level==1 else 'days' if level==2 else 'hours' if level==3 else 'minutes' if level==4 else 'seconds'})")
            print(f"Show offset: {show_offset}")
            break
        elif level == 0:
            level = 5
            show_offset = True
            print(f"All same, defaulting to level {level}")
            print(f"Show offset: {show_offset}")
    
    offset_formats = ['', '%Y', '%Y-%b', '%Y-%b-%d', '%Y-%b-%d', '%Y-%b-%d %H:%M']
    if show_offset and level < len(offset_formats):
        offset_string = test_dates[-1].strftime(offset_formats[level])
        print(f"Offset: '{offset_string}'")
    else:
        print("Offset: (hidden)")

# Test various scenarios
if __name__ == "__main__":
    # Original problem case
    test_date_range(datetime(2021, 2, 14), 200, "Original issue (200 days from 2021-02-14)")
    
    # Span multiple years
    test_date_range(datetime(2020, 11, 1), 400, "Multiple years (400 days from 2020-11-01)")
    
    # Single month
    test_date_range(datetime(2021, 3, 1), 30, "Single month (30 days from 2021-03-01)")
    
    # Multiple months in same year
    test_date_range(datetime(2021, 1, 1), 180, "Multiple months same year (180 days from 2021-01-01)")
    
    # Just a few days
    test_date_range(datetime(2021, 5, 1), 5, "Few days (5 days from 2021-05-01)")