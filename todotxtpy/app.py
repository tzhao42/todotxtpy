"""App logic for the todotxtpy."""

from todotxtpy.constants import CONFIG_PATH, DONE_PATH, TODO_PATH, Colors
from todotxtpy.data import Config, Task, TaskList
from todotxtpy.utils import get_current_date


class TodoApp:
    """The full app for todotxtpy."""

    def __init__(self) -> None:
        """Initialize the app."""
        self.config = Config()
        self.config.load(CONFIG_PATH)
        self.tasklist = TaskList()
        self.tasklist.load(TODO_PATH)
    
    def add(self, priority: str, text: str) -> None:
        """Process raw output and append onto the task list."""
        raw = f"({priority}) {text} {get_current_date()}"
        new_task = Task(raw)
        self.tasklist.tasks.append(new_task)
        self.tasklist.sort()
        self.tasklist.save(TODO_PATH)

    def pri(self, line_number : str, new_priority : str) -> None:
        """Re-prioritize task."""
        idx = int(line_number) - 1
        self.tasklist.tasks[idx].priority = new_priority
        self.tasklist.sort()
        self.tasklist.save(TODO_PATH)

    def do(self, line_number : str) -> None:
        """Complete a task."""
        idx = int(line_number) - 1
        task = self.tasklist.tasks.pop(idx)

        with open(DONE_PATH, mode="a") as file:
            done_task = f"x ({task.priority}) {task.text} {task.tag} {task.creation_date} {get_current_date()}\n"
            file.write(done_task)

        self.tasklist.sort()
        self.tasklist.save(TODO_PATH)

    def rm(self, line_number : str) -> None:
        """Remove a task."""
        idx = int(line_number) - 1
        self.tasklist.tasks.pop(idx)

    def list(self, verbose = False) -> None:
        """Display tasklist."""
        self.tasklist.sort()
        for i, task in enumerate(self.tasklist.tasks):

            # Add line number
            line_number = str(i).zfill(len(str(len(self.tasklist.tasks))))
            display_str = self.config.color_number
            display_str += line_number
            display_str += Colors.ENDC
            display_str += " "

            # Add priority and text
            pri_and_text = f"({task.priority}) {task.text}"
            display_str += self.config.priority_to_color_code(task.priority)
            display_str += pri_and_text
            display_str += Colors.ENDC

            # Add tag, if exists
            if task.tag:
                display_str += " "
                display_str += self.config.color_tag
                display_str += task.tag
                display_str += Colors.ENDC

            # Add date, if verbose
            if verbose:
                display_str += " "
                display_str += self.config.color_date
                display_str += task.creation_date
                display_str += Colors.ENDC

            print(display_str)
