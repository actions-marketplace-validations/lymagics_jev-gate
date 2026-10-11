from hamcrest import assert_that, equal_to, has_entries

from fakes import FakeLines
from jev_gate.span import Span


def test_touches_lines_inside_it():
    assert_that(
        Span("a/b.go", 10, 20).touches(FakeLines({"a/b.go": {20}})),
        equal_to(True),
        "A span must touch its own last line",
    )


def test_ignores_lines_of_other_files():
    assert_that(
        Span("x.c", 1, 99).touches(FakeLines({"y.c": {5}})),
        equal_to(False),
        "A span must not touch another file",
    )


def test_names_file_and_first_line():
    assert_that(
        Span("dir with space/ф.py", 7, 9).properties(),
        has_entries({"file": "dir with space/ф.py", "line": "7"}),
        "A span must give its file and its first line",
    )


def test_prints_as_path_and_line():
    assert_that(
        str(Span("q.rb", 3, 4)), equal_to("q.rb:3"), "A span must print as path:line"
    )
