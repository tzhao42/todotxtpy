# todotxt-py
My personal implementation of a todotxt-like CLI, in Python. I use a customized, restricted subset of the todotxt format:
```
[priority] [creation date%] [tag?] [text]
```
The items marked with a `?` are optional, and the items marked with a `%` are hidden from display (though stored) by default. Upon completion of a task, the app removes the task from `todo.txt` and appends it into `done.txt`, in the following format:
```
x [priority] [creation date] [completion date] [tag?] [text]
```

Supported operations:
* `t add [pri] [tag?] [text]`: add task with `[priority]`, possibly a `[tag?]`, and `[text]`
* `t pri [line] [pri]`: re-prioritize task on `[line]` to `[priority]`
* `t do [line]`: complete task on `[line]`
* `t rm [line]`: remove task on `[line]`, without completing it
* `t list`: list all tasks, in order of priority, creation date, tag, text, with creation date hidden
* `t list verbose`: list all tasks, in order of priority, creation date, tag, text, with creation date included

## Installation Instructions:
Requires `python3.10`; assumes linux. Install with `./install.sh`. I don't personally install like this but this is the way that I'd recommend for someone else.

## Development
I work on the source code in `dev/`, then when it is time to deploy I tie everything up into a large executable file (and a large test file) and dump it all into `todotxtpy/`.

