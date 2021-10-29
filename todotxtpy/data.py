"""Data classes for todotxtpy."""

from functools import cmp_to_key

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
        """Custom comparator for tasks."""

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

    def __init__(self, path: str) -> None:
        """Initialize an Config from a compliant config document."""
        pass
