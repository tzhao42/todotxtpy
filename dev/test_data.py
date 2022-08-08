"""Unittest for data classes."""

import os
import random

import pytest

from constants import DefaultConfig
from data import Config, Task, TaskList
from utils import color_to_color_code


class TestTask:
    """Test Task parsing and equality."""

    def test_01_valid_all(self):
        raw = "(A) 211028 +todotxtpy do lots of epic stuff"
        task = Task.load(raw)
        assert raw == str(task)

    def test_02_valid_notag(self):
        raw = "(A) 211028 todotxtpy do lots of epic stuff"
        task = Task.load(raw)
        assert raw == str(task)

    def test_04_invalid_priority(self):
        raw = "[A) 211028 todotxtpy do lots of epic stuff"
        with pytest.raises(ValueError):
            Task.load(raw)

    def test_05_invalid_priority(self):
        raw = "(!) 211028 todotxtpy do lots of epic stuff"
        with pytest.raises(ValueError):
            Task.load(raw)

    def test_06_invalid_priority(self):
        raw = "(a) 211028 todotxtpy do lots of epic stuff"
        with pytest.raises(ValueError):
            Task.load(raw)

    def test_07_invalid_priority(self):
        raw = "(a|]] 211028 todotxtpy do lots of epic stuff"
        with pytest.raises(ValueError):
            Task.load(raw)

    def test_08_invalid_date(self):
        raw = "(A) 21102 todotxtpy do lots of epic stuff todotxtpy"
        with pytest.raises(ValueError):
            Task.load(raw)

    def test_09_invalid_date(self):
        raw = "(A) 21102d todotxtpy do lots of epic stuff todotxtpy"
        with pytest.raises(ValueError):
            Task.load(raw)

    def test_10_equal(self):
        raw = "(A) 211023 +todotxtpy do lots of epic stuff todotxtpy"
        task_0 = Task.load(raw)
        task_1 = Task.load(raw)
        assert task_0 == task_1

    def test_10_not_equal(self):
        raw_0 = "(A) 211023 +todotxtpy do lots of epic stuff todotxtpy"
        raw_1 = "(A) 211023 +todotxtpy do bots of epic stuff todotxtpy"
        task_0 = Task.load(raw_0)
        task_1 = Task.load(raw_1)
        assert task_0 != task_1


class TestTaskList:
    """Test TaskList loading and saving."""

    def test_01_valid_load(self, tmpdir):
        task_0_raw = "(A) 420420 +tag do things"
        task_1_raw = "(B) 420420 +gat thin"
        path = os.path.join(tmpdir, "testtodo.txt")

        with open(path, "w") as file:
            file.write(f"{task_0_raw}\n{task_1_raw}\n")

        task_list = TaskList.load(path)
        assert len(task_list.tasks) == 2
        assert str(task_list.tasks[0]) == task_0_raw
        assert str(task_list.tasks[1]) == task_1_raw

    def test_02_invalid_load(self, tmpdir):
        task_0_raw = "(A) 420420 +tag do things"
        task_1_raw = "(B) 69696969 +gat thin"
        path = os.path.join(tmpdir, "testtodo.txt")

        with open(path, "w") as file:
            file.write(f"{task_0_raw}\n{task_1_raw}\n")

        with pytest.raises(ValueError):
            TaskList.load(path)

    def test_03_save(self, tmpdir):
        path = os.path.join(tmpdir, "testtodo.txt")
        task_0_raw = "(A) 420420 +tag do things"
        task_1_raw = "(B) 696969 +gat thin"

        task_0 = Task.load(task_0_raw)
        task_1 = Task.load(task_1_raw)

        task_list = TaskList([task_0, task_1])

        task_list.save(path)

        with open(path, "r") as file:
            file_text = file.read()
        assert file_text == f"{task_0_raw}\n{task_1_raw}\n"

    def test_04_sort(self):
        raws = [
            "(A) 012345 +tag text",
            "(A) 012346 +tag text",
            "(A) 012346 +zag text",
            "(A) 012346 +zag zext",
            "(A) 012346 text zag",
            "(A) 012346 zext zag",
            "(B) 012345 +tag text",
            "(B) 012345 +tag text",
        ]

        tasks_sorted = [Task.load(raw) for raw in raws]

        tasks_unsorted = [Task.load(raw) for raw in raws]
        random.shuffle(tasks_unsorted)

        task_list = TaskList(tasks_unsorted)
        task_list.sort()

        assert tasks_sorted == tasks_unsorted


class TestConfig:
    """Test Config loading."""

    def test_01_empty_load(self, tmpdir):
        config_content = ""
        path = os.path.join(tmpdir, "config")

        with open(path, "w") as file:
            file.write(config_content)

        config = Config()
        config.load(path)
        for k, v in DefaultConfig.__dict__.items():
            if k[0] != "_":
                assert config.__dict__[k.lower()] == v

    def test_02_custom_load(self, tmpdir):
        content = {
            "COLOR_PRIORITY_A": "RED",
            "COLOR_PRIORITY_B": "BLUE",
        }
        config_content = "\n".join([f"{k} {v}" for k, v in content.items()]) + "\n"
        path = os.path.join(tmpdir, "config")

        with open(path, "w") as file:
            file.write(config_content)

        config = Config()
        config.load(path)

        for k, v in DefaultConfig.__dict__.items():
            if k[0] != "_":
                if k not in content:
                    assert config.__dict__[k.lower()] == v
                else:
                    assert config.__dict__[k.lower()] == color_to_color_code(content[k])

    def test_03_custom_load_comment(self, tmpdir):
        content = {
            "COLOR_PRIORITY_A": "RED",
            "COLOR_PRIORITY_B": "BLUE",
        }
        config_content = (
            "\n".join([f"{k} {v}" for k, v in content.items()]) + "\n# comment stuff\n"
        )
        path = os.path.join(tmpdir, "config")

        with open(path, "w") as file:
            file.write(config_content)

        config = Config()
        config.load(path)

        for k, v in DefaultConfig.__dict__.items():
            if k[0] != "_":
                if k not in content:
                    assert config.__dict__[k.lower()] == v
                else:
                    assert config.__dict__[k.lower()] == color_to_color_code(content[k])

    def test_04_custom_load_whitespace(self, tmpdir):
        content = {
            "COLOR_PRIORITY_A": "RED",
            "COLOR_PRIORITY_B": "BLUE",
        }
        config_content = (
            "\n".join([f"{k} {v}" for k, v in content.items()]) + "\n\n\n\n"
        )
        path = os.path.join(tmpdir, "config")

        with open(path, "w") as file:
            file.write(config_content)

        config = Config()
        config.load(path)

        for k, v in DefaultConfig.__dict__.items():
            if k[0] != "_":
                if k not in content:
                    assert config.__dict__[k.lower()] == v
                else:
                    assert config.__dict__[k.lower()] == color_to_color_code(content[k])

    def test_05_custom_load_wrong_key_fail(self, tmpdir):
        content = {
            "COLOR_PRIORITY_A": "RED",
            "COLOR_PRIORDTY_B": "BLUE",
        }
        config_content = "\n".join([f"{k} {v}" for k, v in content.items()]) + "\n"
        path = os.path.join(tmpdir, "config")

        with open(path, "w") as file:
            file.write(config_content)

        config = Config()

        with pytest.raises(ValueError):
            config.load(path)

    def test_06_custom_load_wrong_value_fail(self, tmpdir):
        content = {
            "COLOR_PRIORITY_A": "RED",
            "COLOR_PRIORITY_B": "BLLLUE",
        }
        config_content = "\n".join([f"{k} {v}" for k, v in content.items()]) + "\n"
        path = os.path.join(tmpdir, "config")

        with open(path, "w") as file:
            file.write(config_content)

        config = Config()

        with pytest.raises(ValueError):
            config.load(path)
