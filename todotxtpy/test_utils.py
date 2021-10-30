"""Unittest for data classes."""

import pytest

from constants import Colors
from utils import (
    color_to_color_code,
    is_valid_date,
    is_valid_line_number,
    is_valid_priority,
    is_valid_tag,
)


class TestColorToColorcode:
    def test_01_valid_color(self):
        color = "BLACK"
        assert color_to_color_code(color) == Colors.BLACK

    def test_02_invalid_color(self):
        color = "BLLACK"
        with pytest.raises(ValueError):
            color_to_color_code(color)


class TestIsValidPriority:
    def test_01_valid(self):
        raw = "(A)"
        assert is_valid_priority(raw)

    def test_02_invalid_braces(self):
        raw = "[A)"
        assert not is_valid_priority(raw)

    def test_03_invalid_long(self):
        raw = "(A))"
        assert not is_valid_priority(raw)

    def test_04_invalid_middle(self):
        raw = "(!)"
        assert not is_valid_priority(raw)

    def test_05_invalid_middle_long(self):
        raw = "(AA)"
        assert not is_valid_priority(raw)


class TestIsValidDate:
    def test_01_valid(self):
        raw = "012345"
        assert is_valid_date(raw)

    def test_02_invalid(self):
        raw = "012a45"
        assert not is_valid_date(raw)

    def test_03_invalid_short(self):
        raw = "01345"
        assert not is_valid_date(raw)

    def test_04_invalid_long(self):
        raw = "2012345"
        assert not is_valid_date(raw)


class TestIsValidTag:
    def test_01_valid(self):
        raw = "+tag"
        assert is_valid_tag(raw)

    def test_02_invalid(self):
        raw = "tag"
        assert not is_valid_tag(raw)

    def test_03_invalid_empty(self):
        raw = ""
        assert not is_valid_tag(raw)


class TestIsValidLineNumber:
    def test_01_valid(self):
        raw = "1"
        assert is_valid_line_number(raw)

    def test_02_valid_long(self):
        raw = "1234"
        assert is_valid_line_number(raw)

    def test_03_invalid(self):
        raw = "aa"
        assert not is_valid_line_number(raw)
