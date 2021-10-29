"""The main function."""

import sys
from todotxtpy.app import TodoApp

def parse_command(args, app):
    match args:
        case ["add", priority, *text]:
            app.add(priority, " ".join(text))
        case ["pri", line_number, priority]:
            app.pri(line_number, priority)
        case ["do", line_number]:
            app.do(line_number)
        case ["rm", line_number]:
            app.rm(line_number)
        case ["list"]:
            app.list()
        case ["list" "verbose"]:
            app.list(verbose=True)
        case _:
            raise ValueError("Unrecognized command.")

def main():
    """The main operating loop of app."""
    app = TodoApp()
    parse_command(sys.argv[1:], app)

if __name__ == "__main__":
    main()
