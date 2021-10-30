# todotxt-py
My personal implementation of a todotxt-like CLI, in Python. I use a customized, restricted subset of the todotxt format:
```
[priority] [text] [tag?] [creation date%]
```
The items marked with a `?` are optional, and the items marked with a `%` are hidden from display (though stored) by default. Upon completion of a task, the app removes the task from `todo.txt` and appends it into `done.txt`, in the following format:
```
x [priority] [text] [tag?] [creation date] [completion date]
```

Supported operations:
* `t add [pri] [tag?] [text]`: add task with `[priority]`, possibly a `[tag?]`, and `[text]`
* `t pri [line] [pri]`: re-prioritize task on `[line]` to `[priority]`
* `t do [line]`: complete task on `[line]`
* `t rm [line]`: remove task on `[line]`, without completing it
* `t list`: list all tasks, in order of priority, creation date, tag, text, with creation date hidden
* `t list verbose`: list all tasks, in order of priority, creation date, tag, text, with creation date included

## Installation Instructions:
Requires `python3.10`; assumes linux.
```
mkdir ~/todo
touch ~/todo/config
touch ~/todo/todo.txt
touch ~/todo/done.txt
cd ~
git clone git@github.com:tzhao42/todotxtpy.git
echo "alias t='python3.10 /home/$USER/todotxtpy/main.py'" >> /home/$USER/.bash_aliases
```
That's it.
