"""Data classes for todotxtpy."""

from functools import cmp_to_key

from constants import DefaultConfig
from utils import (
    color_to_color_code,
    is_valid_date,
    is_valid_priority,
    is_valid_tag,
)


class Task:
    """Simple task class."""

    def __init__(self) -> None:
        """Initialize empty Task."""
        # Type hinting
        self.priority: str = None  # "([capital letter])"
        self.creation_date: str = None
        self.tag: str = None
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
