"""Constants for todotxtpy."""

class Colors:
    """ANSI escape sequences for colors."""

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GREY = "\033[0;37m"
    DARK_GREY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"
    DEFAULT = "\033[0m"

    # Non-color options
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"

class DefaultConfig:
    """Default settings."""

    COLOR_PRIORITY_A = Colors.YELLOW
    COLOR_PRIORITY_B = Colors.BROWN
    COLOR_PRIORITY_C = Colors.GREEN
    COLOR_PRIORITY_D = Colors.BLUE
    COLOR_PRIORITY_E = Colors.CYAN
    COLOR_PRIORITY_REST = Colors.WHITE

    COLOR_TAG = Colors.LIGHT_BLUE
    COLOR_DATE = Colors.LIGHT_PURPLE
    COLOR_NUMBER = Colors.DARK_GREY

    TODO_TXT_PATH = None # Must be overridden
    DONE_TXT_PATH = None # Must be overridden
