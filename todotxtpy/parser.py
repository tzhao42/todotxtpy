"""Argument parser for todotxtpy."""

def parse(args):

    # match is so nice...
    match args:

        case ["add", raw_text]:
            print(f"adding {raw_text}...")

        case ["pri", line_number, priority]:
            print(f"priority {line_number} {priority}...")

        case ["add", "pri", priority, raw_text]:
            print(f"add {raw_text} with priority {priority}...")

        case ["do", line_number]:
            print(f"doing {line_number}...")

        case ["rm", line_number]:
            print(f"removing {line_number}...")

        case ["list"]:
            print("listing...")

        case _:
            print("unrecognized input")

if __name__ == "__main__":
    import sys
    parse(sys.argv[1:])
