"""Utility functions for todotxtpy."""

import datetime

from todotxtpy.constants import Colors


def get_current_date():
    """Return date in form of yymmdd."""
    return datetime.datetime.now().strftime("%y%m%d")

def color_to_color_code(color : str) -> str:
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

if __name__ == "__main__":
    print(get_current_date())
