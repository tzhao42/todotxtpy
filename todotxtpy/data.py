"""Data classes for todotxtpy."""

from functools import cmp_to_key

from todotxtpy.constants import DefaultConfig
from todotxtpy.utils import color_to_color_code


class Task:
    """Simple task class."""

    def __init__(self, line: str) -> None:
        """Initialize a Task from the text of a line
        
        Expected format is 
        "[priority] [text] [tag?] [creation date%]"
        """

        # Type hinting
        self.priority: str # a single letter
        self.text: str
        self.tag: str
        self.creation_date: str

        # Parse line
        tokens = line.split()

        # Recognized priority
        first_token = tokens.pop(0)
        match [l for l in first_token]:
            case ["(", priority, ")"]:
                if not priority.isupper():
                    raise ValueError("Unsupported priority.")
                
                self.priority = priority
            case _:
                raise ValueError("Unrecognized format.")
        
        # Recognize creation date
        last_token = tokens.pop()
        if len(last_token) == 6 and last_token.isdecimal():
            self.creation_date = last_token
        else:
            raise ValueError("Unrecognized format.")
        
        # Recognize tag, if present
        self.tag = tokens.pop() if tokens[-1][0] == "+" else None
        
        # Dump rest of text in text field
        self.text = " ".join(tokens)

    def __str__(self) -> str:
        # This is used for saving, display is handeled differently
        ret = ""
        ret += f"({self.priority}) {self.text} "
        if self.tag:
            ret += self.tag + " "
        ret += self.creation_date
        return ret

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return self.__dict__ == o.__dict__
        else:
            return False


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
                task = Task(line.rstrip())
                self.tasks.append(task)

    def save(self, path: str) -> None:
        """Save TaskList to file specified by path.

        If file already exists, overwrites file completely.
        """
        with open(path, mode='w') as f:
            for task in self.tasks:
                f.write(f"{str(task)}\n")

    def sort(self) -> None:
        """Sort TaskList in order of priority, creation date, tag, text.
        
        Entries without tag come last; otherwise everything is string order.
        """
        self.tasks.sort(key=cmp_to_key(self._compare))

    def _compare(self, task1: Task, task2: Task) -> int:
        """Custom comparator for sorting tasks."""

        # Compare priorities
        if task1.priority < task2.priority:
            return -1
        elif task1.priority > task2.priority:
            return 1

        # Priorities equal, compare creation date
        if task1.creation_date < task2.creation_date:
            return -1
        elif task1.creation_date > task2.creation_date:
            return 1

        # Creation dates equal, compare tags
        if task1.tag and (not task2.tag):
            return -1
        elif (not task1.tag) and task2.tag:
            return 1
        elif task1.tag and task2.tag:
            if task1.tag < task2.tag:
                return -1
            elif task1.tag > task2.tag:
                return 1

        # Tags equal, compare text
        if task1.text < task2.text:
            return -1
        elif task1.text > task2.text:
            return 1
        
        # Everything equal
        return 0


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
                    case ["COLOR_DATA", color]:
                        self.color_data = color_to_color_code(color)
                    case ["COLOR_NUMBER", color]:
                        self.color_number = color_to_color_code(color)
                    case _:
                        print(setting)
                        raise ValueError("Setting not recognized")

        
    def priority_to_color_code(self, priority : str) -> str:
        match priority:
            case "A":
                return self.color_priority_a
            case "B":
                return self.color_priority_b
            case "C":
                return self.color_priority_c
            case "D":
                return self.color_priority_d
            case "E":
                return self.color_priority_e
            case _:
                return self.color_priority_rest

