#!/bin/python3.10

"""Full executable file."""

import os
import sys
import datetime
from functools import cmp_to_key
from typing import Optional

# Constants

TODO_DIRECTORY = os.path.join(os.path.expanduser("~"), "todo")
CONFIG_PATH = os.path.join(TODO_DIRECTORY, "config")
TODO_PATH = os.path.join(TODO_DIRECTORY, "todo.txt")
DONE_PATH = os.path.join(TODO_DIRECTORY, "done.txt")


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


# Data


class Task:
    """Simple task class."""

    def __init__(self) -> None:
        """Initialize empty Task."""
        # Type hinting
        self.priority: str = None  # "([capital letter])"
        self.creation_date: str = None
        self.tag: Optional[str] = None
        self.text: str = None

    def load(self, line: str) -> None:
        """Populate fields of a Task from the text of a line.

        Expected format is
        "[priority] [creation date%] [tag?] [text]"
        """
        tokens = line.split()

        # Recognize priority
        head = tokens.pop(0)
        if is_valid_priority(head):
            self.priority = head
        else:
            raise ValueError("Unrecognized format.")

        # Recognize creation date
        head = tokens.pop(0)
        if is_valid_date(head):
            self.creation_date = head
        else:
            raise ValueError("Unrecognized format.")

        # Recognize tag, if present
        head = tokens[0]
        if is_valid_tag(head):
            self.tag = tokens.pop(0)

        # Dump rest of text in text field
        self.text = " ".join(tokens)

    def __str__(self) -> str:
        # This is used for saving, display is handeled differently
        elements = [self.priority, self.creation_date, self.text]
        if self.tag:
            elements.insert(2, self.tag)
        return " ".join(elements)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, self.__class__) and self.__dict__ == o.__dict__


class TaskList:
    """List of tasks."""

    def __init__(self) -> None:
        """Initialize a TaskList."""
        self.tasks = []

    def load(self, path: str) -> None:
        """Append tasks from file to TaskList."""
        with open(path, mode="r") as file:
            lines = file.readlines()
            for line in lines:
                if line != "\n":
                    task = Task()
                    task.load(line.rstrip())
                    self.tasks.append(task)

    def save(self, path: str) -> None:
        """Save TaskList to file specified by path.

        If file already exists, overwrites file completely.
        """
        with open(path, mode="w") as file:
            for task in self.tasks:
                file.write(f"{str(task)}\n")

    def sort(self) -> None:
        """Sort TaskList in order of priority, creation date, tag, text.

        Entries without tag come last; otherwise everything is string order.
        """
        self.tasks.sort(key=cmp_to_key(task_compare))


class Config:
    """User config."""

    def __init__(self) -> None:
        """Initialize a Config from a compliant config document."""

        self.color_priority_a = DefaultConfig.COLOR_PRIORITY_A
        self.color_priority_b = DefaultConfig.COLOR_PRIORITY_B
        self.color_priority_c = DefaultConfig.COLOR_PRIORITY_C
        self.color_priority_d = DefaultConfig.COLOR_PRIORITY_D
        self.color_priority_e = DefaultConfig.COLOR_PRIORITY_E
        self.color_priority_rest = DefaultConfig.COLOR_PRIORITY_REST

        self.color_tag = DefaultConfig.COLOR_TAG
        self.color_date = DefaultConfig.COLOR_DATE
        self.color_number = DefaultConfig.COLOR_NUMBER

    def load(self, path: str) -> None:
        """Append tasks from file to TaskList."""
        with open(path, mode="r") as file:
            lines = file.readlines()
            for line in lines:
                setting = line.rstrip().split()
                match setting:
                    case ["COLOR_PRIORITY_A", color]:
                        self.color_priority_a = color_to_color_code(color)
                    case ["COLOR_PRIORITY_B", color]:
                        self.color_priority_b = color_to_color_code(color)
                    case ["COLOR_PRIORITY_C", color]:
                        self.color_priority_c = color_to_color_code(color)
                    case ["COLOR_PRIORITY_D", color]:
                        self.color_priority_d = color_to_color_code(color)
                    case ["COLOR_PRIORITY_E", color]:
                        self.color_priority_e = color_to_color_code(color)
                    case ["COLOR_PRIORITY_REST", color]:
                        self.color_priority_rest = color_to_color_code(color)
                    case ["COLOR_TAG", color]:
                        self.color_tag = color_to_color_code(color)
                    case ["COLOR_DATE", color]:
                        self.color_date = color_to_color_code(color)
                    case ["COLOR_NUMBER", color]:
                        self.color_number = color_to_color_code(color)
                    case ["#", *_]:
                        # Comment
                        pass
                    case []:
                        # Whitespace
                        pass
                    case _:
                        print(setting)
                        raise ValueError("Setting not recognized")

    def priority_to_color_code(self, priority : str) -> str:
        """Return color code corresponding to a certain priority."""
        match priority:
            case "(A)":
                return self.color_priority_a
            case "(B)":
                return self.color_priority_b
            case "(C)":
                return self.color_priority_c
            case "(D)":
                return self.color_priority_d
            case "(E)":
                return self.color_priority_e
            case _:
                return self.color_priority_rest


# Utils


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


def task_compare(task1: Task, task2: Task) -> int:
    """Custom comparator for sorting tasks."""

    # Compare priorities
    if task1.priority < task2.priority:
        return -1
    if task1.priority > task2.priority:
        return 1

    # Priorities equal, compare tag
    if task1.tag and (not task2.tag):
        return -1
    if (not task1.tag) and task2.tag:
        return 1
    if task1.tag and task2.tag:
        if task1.tag < task2.tag:
            return -1
        if task1.tag > task2.tag:
            return 1

    # Tags equal, compare creation date
    if task1.creation_date < task2.creation_date:
        return -1
    if task1.creation_date > task2.creation_date:
        return 1

    # Tags equal, compare text
    if task1.text < task2.text:
        return -1
    if task1.text > task2.text:
        return 1

    # Everything equal
    return 0


# App


class TodoApp:
    """The full app for todotxtpy."""

    def __init__(self, config_path, todo_path, done_path) -> None:
        """Initialize the app."""
        self.config = Config()
        self.config.load(config_path)
        self.tasklist = TaskList()
        self.tasklist.load(todo_path)

        self.config_path = config_path
        self.todo_path = todo_path
        self.done_path = done_path

    def add(self, priority: str, tag: str, text: str) -> None:
        """Process raw output and append onto the task list."""
        new_task = Task()
        new_task.priority = priority
        new_task.creation_date = get_current_date()
        new_task.tag = tag
        new_task.text = text

        self.tasklist.tasks.append(new_task)

        self.tasklist.sort()
        self.tasklist.save(self.todo_path)

    def pri(self, line_number: str, new_priority: str) -> None:
        """Re-prioritize task."""
        idx = int(line_number) - 1

        if not 0 <= idx <= len(self.tasklist.tasks) - 1:
            raise ValueError("Line number out of range")

        self.tasklist.tasks[idx].priority = new_priority

        self.tasklist.sort()
        self.tasklist.save(self.todo_path)

    def do_task(self, line_number: str) -> None:
        """Complete a task."""
        idx = int(line_number) - 1

        if not 0 <= idx <= len(self.tasklist.tasks) - 1:
            raise ValueError("Line number out of range")

        task = self.tasklist.tasks.pop(idx)

        with open(self.done_path, mode="a") as file:
            done_task = "x "
            done_task += task.priority + " "
            done_task += task.creation_date + " "
            done_task += get_current_date() + " "
            if task.tag:
                done_task += task.tag + " "
            done_task += task.text + "\n"
            file.write(done_task)

        self.tasklist.sort()
        self.tasklist.save(self.todo_path)

    def remove_task(self, line_number: str) -> None:
        """Remove a task."""
        idx = int(line_number) - 1

        if not 0 <= idx <= len(self.tasklist.tasks) - 1:
            raise ValueError("Line number out of range")

        self.tasklist.tasks.pop(idx)

        self.tasklist.sort()
        self.tasklist.save(self.todo_path)

    def list(self, verbose=False) -> None:
        """Display tasklist."""
        self.tasklist.sort()
        for i, task in enumerate(self.tasklist.tasks):

            # Add line number
            line_number = str(i + 1).zfill(len(str(len(self.tasklist.tasks))))
            display_str = self.config.color_number
            display_str += line_number
            display_str += Colors.ENDC

            display_str += " "

            # Add priority
            display_str += self.config.priority_to_color_code(task.priority)
            display_str += task.priority
            display_str += Colors.ENDC

            # Add date, if verbose
            if verbose:
                display_str += " "
                display_str += self.config.color_date
                display_str += task.creation_date
                display_str += Colors.ENDC

            # Add tag, if exists
            if task.tag:
                display_str += " "
                display_str += self.config.color_tag
                display_str += task.tag
                display_str += Colors.ENDC

            # Add text
            display_str += " "
            display_str += self.config.priority_to_color_code(task.priority)
            display_str += task.text
            display_str += Colors.ENDC

            print(display_str)


# Main


def parse_command(args, app):
    """Parse command from command line."""
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

            app.do_task(line_number)

        case ["rm", line_number]:

            if not is_valid_line_number(line_number):
                raise ValueError("Unrecognized line number.")

            app.remove_task(line_number)

        case ["list"]:
            app.list()

        case ["list", "verbose"]:
            app.list(verbose=True)

        case ["help"]:
            print("Supported operations:\n"
            + "t add [pri] [tag?] [text]: add task with [priority], possibly a [tag?], and [text]\n"
            + "t pri [line] [pri]: re-prioritize task on [line] to [priority]\n"
            + "t do [line]: complete task on [line]\n"
            + "t rm [line]: remove task on [line], without completing it\n"
            + "t list: list all tasks, in order of priority, creation date, tag, text, with creation date hidden\n"
            + "t list verbose: list all tasks, in order of priority, creation date, tag, text, with creation date included\n")

        case _:
            raise ValueError("Unrecognized command.")


def main():
    """The main operating loop of app."""
    app = TodoApp(CONFIG_PATH, TODO_PATH, DONE_PATH)
    parse_command(sys.argv[1:], app)


if __name__ == "__main__":
    main()
