#!/usr/bin/env python3
"""
Test case for the ConciseDateFormatter fix.
This test can be added to test_dates.py to ensure the bug doesn't regress.
"""

def test_concise_formatter_monthly_ticks_show_year():
    """
    Test that monthly ticks show the year in the offset.
    
    This addresses the issue where ConciseDateFormatter was hiding 
    the year offset for monthly ticks, making it unclear what year
    the months belonged to.
    
    See: https://github.com/matplotlib/matplotlib/issues/22871
    """
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import datetime
    
    # Create a date range that would trigger monthly ticks
    d1 = datetime.datetime(2021, 2, 1)
    d2 = datetime.datetime(2021, 9, 1)
    
    fig, ax = plt.subplots()
    locator = mdates.AutoDateLocator(minticks=3, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    # Plot data that spans several months
    ax.plot([d1, d2], [0, 1])
    ax.set_xlim(d1, d2)
    fig.draw_without_rendering()
    
    # When monthly ticks are chosen, the year should be shown in the offset
    offset = formatter.get_offset()
    
    # The offset should contain the year (2021) to provide context
    # It might be '2021' or '2021-Sep' depending on the exact formatting
    assert '2021' in offset, f"Expected year '2021' in offset, got '{offset}'"
    
    plt.close(fig)

def test_concise_formatter_yearly_ticks_hide_offset():
    """
    Test that yearly ticks still correctly hide the offset.
    
    This ensures the fix doesn't break the existing behavior
    for yearly ticks where showing the year in the offset
    would be redundant.
    """
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import datetime
    
    # Create a date range that spans multiple years
    d1 = datetime.datetime(2019, 1, 1)
    d2 = datetime.datetime(2023, 1, 1)
    
    fig, ax = plt.subplots()
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    # Plot data that spans several years
    ax.plot([d1, d2], [0, 1])
    ax.set_xlim(d1, d2)
    fig.draw_without_rendering()
    
    # For yearly ticks, offset should be empty since years are already
    # shown in the tick labels
    offset = formatter.get_offset()
    assert offset == '', f"Expected empty offset for yearly ticks, got '{offset}'"
    
    plt.close(fig)

if __name__ == "__main__":
    # These tests would normally be run by pytest, but we can't easily 
    # run them here due to matplotlib import issues
    print("Test definitions created. These should be added to test_dates.py")
    print("They test:")
    print("1. Monthly ticks show year in offset (the fix)")
    print("2. Yearly ticks still hide offset (regression check)")