"""Utility functions for todotxtpy."""

import datetime

from todotxtpy.data import Task
from todotxtpy.constants import Priority


def get_current_date():
    """Return date in form of yymmdd."""
    return datetime.datetime.now().strftime("%y%m%d")

if __name__ == "__main__":
    print(get_current_date())
