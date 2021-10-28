"""Utility functions for todotxtpy."""

import datetime

def get_current_date():
    """Return date in form of yymmdd."""
    return datetime.datetime.now().strftime("%y%m%d")


if __name__ == "__main__":
    print(get_current_date())