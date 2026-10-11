from hamcrest import assert_that, empty, equal_to

from fakes import FakeLines
from jev_gate.sha import Sha


def test_touches_any_change():
    assert_that(
        Sha("0" * 40).touches(FakeLines({})),
        equal_to(True),
        "A commit must count as touched by its own change",
    )


def test_names_no_file():
    assert_that(Sha("deadbeef").properties(), empty(), "A commit must name no file")


def test_prints_short_digest():
    assert_that(
        str(Sha("abcdef0123456789abcdef")),
        equal_to("commit abcdef012345"),
        "A commit must print a twelve-digit digest",
    )
