"""Data classes for todotxtpy."""

class Task:
    """Simple task class."""

    def __init__(self, line: str) -> None:
        """Initialize a Task from the text of a line
        
        Expected format is 
        "[priority] [text] [tag?] [creation date%]"
        """

        # Type hinting
        self.priority: str
        self.text: str
        self.tag: str
        self.creation_date: str

        # Parse line
        tokens = line.split()

        self.priority = tokens.pop(0)[1]
        assert self.priority.isupper(), "Invalid priority."

        self.creation_date = tokens.pop()
        assert len(self.creation_date) == 6, "Invalid creation date."

        self.tag = tokens.pop() if tokens[-1][0] == "+" else None
        
        # Dump rest of text in text field
        self.text = " ".join(tokens)


    def __str__(self) -> str:
        # This is only used for debuging, actual display is handeled by the app
        ret = ""
        ret += f"({self.priority}) {self.text} "
        if self.tag:
            ret += self.tag + " "
        ret += self.creation_date
        return ret


class TaskList:
    """List of tasks."""

    def __init__(self, path: str) -> None:
        """Initialize a TaskList."""
        self.tasks = []

    def load(self, path: str) -> None:
        """Populate TaskList from a compliant todo document specified by path."""
        pass

    def save(self, path: str) -> None:
        """Save TaskList to file specified by path.

        If file already exists, overwrites file completely.
        """
        pass


class Config:
    """User config."""

    def __init__(self, path: str) -> None:
        """Initialize an Config from a compliant config document."""
        pass

if __name__ == "__main__":

    # Testing
    rawline = "(A) do lots of epic stuff +todotxtpy 211028"
    task = Task(rawline)
    assert str(task) == rawline

    rawline = "(A) do lots of epic stuff for todotxtpy 211028"
    task = Task(rawline)
    assert str(task) == rawline

    rawline = "(A) do lots of epic stuff for todotxtpy 21102"
    try:
        task = Task(rawline)
        raise ValueError("Failed test, invalid date got through")
    except AssertionError:
        pass

    rawline = "(!) do lots of epic stuff for todotxtpy 211026"
    try:
        task = Task(rawline)
        raise ValueError("Failed test, invalid priority got through")
    except AssertionError:
        pass

    print("Tests passed")
