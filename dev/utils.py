"""Utility functions for todotxtpy."""

import datetime

from constants import Colors


def get_current_date():
    """Return date in form of yymmdd."""
    return datetime.datetime.now().strftime("%y%m%d")


def color_to_color_code(color: str) -> str:
    """Convert color to color code."""
    match color:
        case "BLACK" :
            return Colors.BLACK
        case "RED" :
            return Colors.RED
        case "GREEN" :
            return Colors.GREEN
        case "BROWN" :
            return Colors.BROWN
        case "BLUE" :
            return Colors.BLUE
        case "PURPLE" :
            return Colors.PURPLE
        case "CYAN" :
            return Colors.CYAN
        case "LIGHT_GREY" :
            return Colors.LIGHT_GREY
        case "DARK_GREY" :
            return Colors.DARK_GREY
        case "LIGHT_RED" :
            return Colors.LIGHT_RED
        case "LIGHT_GREEN" :
            return Colors.LIGHT_GREEN
        case "YELLOW" :
            return Colors.YELLOW
        case "LIGHT_BLUE" :
            return Colors.LIGHT_BLUE
        case "LIGHT_PURPLE" :
            return Colors.LIGHT_PURPLE
        case "LIGHT_CYAN" :
            return Colors.LIGHT_CYAN
        case "WHITE" :
            return Colors.WHITE
        case "DEFAULT" :
            return Colors.DEFAULT
        case "BOLD" :
            return Colors.BOLD
        case "UNDERLINE" :
            return Colors.UNDERLINE
        case "ENDC" :
            return Colors.ENDC
        case _:
            raise ValueError("Unrecognized color.")


def is_valid_priority(priority: str) -> bool:
    """Return whether input is a valid priority."""
    match list(priority):
        case ["(", letter, ")"]:
            return letter.isupper()
        case _:
            return False


def is_valid_date(date: str) -> bool:
    """Return whether input is a valid date."""
    return len(date) == 6 and date.isdecimal()


def is_valid_tag(tag: str) -> bool:
    """Return whether input is a valid tag."""
    return len(tag) > 0 and tag[0] == "+"


def is_valid_line_number(line_number: str) -> bool:
    """Return whether input isa valid line number."""
    return line_number.isdecimal()
