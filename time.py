"""
Examine this code.

- Is it easy to verify that it works correctly?
- Do you see any obvious errors?
- How would you modify it to be easier to read?
"""

import datetime

def createTimeFromTimestamp(timestamp):
    """Create a datetime.time object from a timestamp string.

    The timestamp is in the format 'hh:mm:ss'.

    >>> t = createTimeFromTimestamp("9:23:15")
    >>> type(t)
    <class 'datetime.time'>
    >>> print(t)
    09:23:15
    """
    args = timestamp.split(":")
    if len(args) != 3:
        return None
    try:
        if 0 <= int(args[0]) <= 23 and 0 <= int(args[1]) < 60 and 0 <= int(args[2]) < 60:
            return datetime.time(int(args[0]), int(args[1])), int(args[2]))
    except ValueError:
        return None
