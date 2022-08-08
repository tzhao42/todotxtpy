"""App logic for the todotxtpy."""

from constants import Colors
from data import Config, Tag, Task, TaskList
from utils import get_current_date


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

    def add(self, priority: str, tag: Tag, text: str) -> None:
        """Process raw output and append onto the task list."""
        new_task = Task(priority, get_current_date(), tag, text)

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
            if task.tag.tag is not None:
              done_task += task.tag.tag + " "
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
            if task.tag.tag is not None:
                display_str += " "
                display_str += self.config.color_tag
                display_str += task.tag.tag
                display_str += Colors.ENDC

            # Add text
            display_str += " "
            display_str += self.config.priority_to_color_code(task.priority)
            display_str += task.text
            display_str += Colors.ENDC

            print(display_str)
