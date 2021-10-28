# todotxt-py
My personal implementation of a todotxt-like CLI, in Python. I use a customized, restricted subset of the todotxt format:
```
[priority] [text] [tags?] [creation date%]
```
The items marked with a `?` are optional, and the items marked with a `%` are hidden from display (though stored) by default. Upon completion of a task, the app removes the task from `todo.txt` and appends it into `done.txt`, in the following format:
```
x [priority] [text] [tags?] [creation date] [completion date]
```
