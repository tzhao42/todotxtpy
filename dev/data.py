"""Data classes for todotxtpy."""

from __future__ import annotations
from dataclasses import dataclass
from functools import total_ordering
from typing import Optional

from constants import DefaultConfig
from utils import (
    color_to_color_code,
    is_valid_date,
    is_valid_priority,
    is_valid_tag,
)

# explicitly define Tags as a class for custom ordering
@total_ordering
@dataclass
class Tag:
    """A tag for a Task."""
    tag: Optional[str]

    def __gt__(self, other):
        # None tags sort towards the end
        if self.tag is None: return True
        if other.tag is None: return False
        return self.tag > other.tag


@dataclass(order=True)
class Task:
    """Simple task class."""
    priority: str # "([capital letter])"
    creation_date: str
    tag: Tag
    text: str

    @classmethod
    def load(cls, line: str) -> Task:
        """Populate fields of a Task from the text of a line.

        Expected format is
        "[priority] [creation date%] [tag?] [text]"
        """
        priority, creation_date, *rest = line.split()

        if not is_valid_priority(priority):
            raise ValueError(f"Unrecognized priority {priority}.")
        if not is_valid_date(creation_date):
            raise ValueError(f"Unrecognized date {creation_date}.")

        if len(rest) > 0 and is_valid_tag(rest[0]):
            tag, *text_words = rest
            text = ' '.join(text_words)
        else:
            tag = None
            text = ' '.join(rest)

        return Task(priority, creation_date, Tag(tag), text)


    def __str__(self) -> str:
        # This is used for saving, display is handled differently
        elements = [self.priority, self.creation_date, self.text]
        if self.tag.tag:
            elements.insert(2, self.tag.tag)
        return " ".join(elements)


class TaskList:
    """List of tasks."""

    def __init__(self) -> None:
        """Initialize a TaskList."""
        self.tasks: list[Task] = []

    def load(self, path: str) -> None:
        """Append tasks from file to TaskList."""
        with open(path, mode="r") as file:
            lines = file.readlines()
            for line in lines:
                if line != "\n":
                    task = Task.load(line.rstrip())
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
        self.tasks.sort()


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
