"""Unittest for tasks."""

import os
import pytest

from todotxtpy.data import Task, TaskList


class TestTask:
    """Test Task parsing and equality."""

    def test_01_valid_all(self):
        raw = "(A) do lots of epic stuff +todotxtpy 211028"
        task = Task(raw)
        assert raw == str(task)

    def test_02_valid_notag(self):
        raw = "(A) do lots of epic stuff todotxtpy 211028"
        task = Task(raw)
        assert raw == str(task)

    def test_04_invalid_priority(self):
        raw = "[A) do lots of epic stuff todotxtpy 211028"
        with pytest.raises(ValueError):
            task = Task(raw)

    def test_05_invalid_priority(self):
        raw = "(!) do lots of epic stuff todotxtpy 211028"
        with pytest.raises(ValueError):
            task = Task(raw)

    def test_06_invalid_priority(self):
        raw = "(a) do lots of epic stuff todotxtpy 211028"
        with pytest.raises(ValueError):
            task = Task(raw)

    def test_07_invalid_priority(self):
        raw = "(a|]] do lots of epic stuff todotxtpy 211028"
        with pytest.raises(ValueError):
            task = Task(raw)

    def test_08_invalid_date(self):
        raw = "(A) do lots of epic stuff todotxtpy 21102"
        with pytest.raises(ValueError):
            task = Task(raw)

    def test_09_invalid_date(self):
        raw = "(A) do lots of epic stuff todotxtpy 21102a"
        with pytest.raises(ValueError):
            task = Task(raw)

    def test_10_equal(self):
        raw = "(A) do lots of epic stuff todotxtpy 211023"
        task_0 = Task(raw)
        task_1 = Task(raw)
        assert task_0 == task_1

    def test_10_not_equal(self):
        raw_0 = "(A) do lots of epic stuff todotxtpy 211023"
        raw_1 = "(A) do bots of epic stuff todotxtpy 211023"
        task_0 = Task(raw_0)
        task_1 = Task(raw_1)
        assert task_0 != task_1


class TestTaskList:
    """Test TaskList loading and saving."""

    def test_01_valid_load(self, tmpdir):
        task_0_raw = "(A) do things +tag 420420"
        task_1_raw = "(B) thin +gat 696969"
        path = os.path.join(tmpdir, "testtodo.txt")

        with open(path, "w") as file:
            file.write(f"{task_0_raw}\n{task_1_raw}\n")

        task_list = TaskList()
        task_list.load(path)
        assert len(task_list.tasks) == 2
        assert str(task_list.tasks[0]) == task_0_raw
        assert str(task_list.tasks[1]) == task_1_raw

    def test_02_invalid_load(self, tmpdir):
        task_0_raw = "(A) do things +tag 420420"
        task_1_raw = "(B) thin +gat 6969696969"
        path = os.path.join(tmpdir, "testtodo.txt")

        with open(path, "w") as file:
            file.write(f"{task_0_raw}\n{task_1_raw}\n")

        task_list = TaskList()
        with pytest.raises(ValueError):
            task_list.load(path)

    def test_03_save(self, tmpdir):
        path = os.path.join(tmpdir, "testtodo.txt")
        task_0_raw = "(A) do things +tag 420420"
        task_1_raw = "(B) thin +gat 696969"

        task_0 = Task(task_0_raw)
        task_1 = Task(task_1_raw)

        task_list = TaskList()
        task_list.tasks.append(task_0)
        task_list.tasks.append(task_1)

        task_list.save(path)

        with open(path, "r") as file:
            file_text = file.read()
        print(file_text)
        assert file_text == f"{task_0_raw}\n{task_1_raw}\n"

    def test_04_sort(self):
        raws = [
            "(A) text +tag 012345",
            "(A) text +tag 012346",
            "(A) text +zag 012346",
            "(A) zext +zag 012346",
            "(A) text zag 012346",
            "(A) zext zag 012346",
            "(B) text +tag 012345",
            "(B) text +tag 012345",
        ]
        tasks = [Task(raw) for raw in raws]
        tasks.reverse()

        task_list = TaskList()
        for task in tasks:
            task_list.tasks.append(task)
        task_list.sort()

        tasks.reverse()
        for i, task in enumerate(tasks):
            assert task == task_list.tasks[i]
