import io

from hamcrest import assert_that, equal_to

from jev_gate.anywhere import Anywhere
from jev_gate.github_log import GithubLog
from jev_gate.span import Span


def test_writes_an_error_annotation():
    stream = io.StringIO()
    GithubLog(stream).error(Span("src/a.py", 12, 14), "gate-1", "fired at 0.95")
    assert_that(
        stream.getvalue(),
        equal_to("::error file=src/a.py,line=12,title=gate-1::fired at 0.95\n"),
        "An error must become a GitHub error annotation",
    )


def test_writes_a_warning_without_file():
    stream = io.StringIO()
    GithubLog(stream).warning(Anywhere("x"), "gate-2", "left out 3")
    assert_that(
        stream.getvalue(),
        equal_to("::warning title=gate-2::left out 3\n"),
        "A warning without a place must carry only a title",
    )


def test_escapes_special_characters():
    stream = io.StringIO()
    GithubLog(stream).error(Span("we,ird:name.py", 1, 1), "t", "100%\nsure\r")
    assert_that(
        stream.getvalue(),
        equal_to("::error file=we%2Cird%3Aname.py,line=1,title=t::100%25%0Asure%0D\n"),
        "Workflow command data and properties must be escaped",
    )


def test_writes_plain_info():
    stream = io.StringIO()
    GithubLog(stream).info("jev-gate: 0 verdicts")
    assert_that(
        stream.getvalue(), equal_to("jev-gate: 0 verdicts\n"), "Info must be plain text"
    )
