"""Data classes for todotxtpy."""

class Task:
    """Simple task class."""

    def __init__(self) -> None:
        """Initialize an empty Task."""
        self.priority = None
        self.date = None
        self.text = None
        self.tags = None
        self.line_number = None

class TaskList:
    """List of tasks."""

    def __init__(self, path:str) -> None:
        """Initialize a TaskList from a compliant todo document, specified by a config."""
        pass

    def save(self, path:str) -> None:
        """Save tasklist to file specified by path."""
        pass

class Config:
    """User config."""

    def __init__(self, path:str) -> None:
        """Initialize an Config from a compliant config document."""
        pass

