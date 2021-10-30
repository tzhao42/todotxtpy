"""The main function."""

import sys

from todotxtpy.app import TodoApp
from todotxtpy.constants import CONFIG_PATH, DONE_PATH, TODO_PATH
from todotxtpy.utils import (
    is_valid_line_number,
    is_valid_priority,
    is_valid_tag,
)


def parse_command(args, app):
    match args:

        case ["add", raw_priority, *text]:

            priority = "(" + raw_priority + ")"
            if not is_valid_priority(priority):
                raise ValueError("Unrecognized priority.")

            if is_valid_tag(text[0]):
                tag = text.pop(0)
                app.add(priority, tag, " ".join(text))
            else:
                app.add(priority, None, " ".join(text))

        case ["pri", line_number, raw_priority]:

            if not is_valid_line_number(line_number):
                raise ValueError("Unrecognized line number.")

            priority = "(" + raw_priority + ")"
            if not is_valid_priority(priority):
                raise ValueError("Unrecognized priority.")

            app.pri(line_number, priority)

        case ["do", line_number]:

            if not is_valid_line_number(line_number):
                raise ValueError("Unrecognized line number.")

            app.do(line_number)

        case ["rm", line_number]:

            if not is_valid_line_number(line_number):
                raise ValueError("Unrecognized line number.")

            app.rm(line_number)

        case ["list"]:
            app.list()

        case ["list", "verbose"]:
            app.list(verbose=True)

        case _:
            raise ValueError("Unrecognized command.")


def main():
    """The main operating loop of app."""
    app = TodoApp(CONFIG_PATH, TODO_PATH, DONE_PATH)
    parse_command(sys.argv[1:], app)


if __name__ == "__main__":
    main()
