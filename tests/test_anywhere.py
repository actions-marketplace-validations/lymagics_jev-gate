from hamcrest import assert_that, empty, equal_to

from fakes import FakeLines
from jev_gate.anywhere import Anywhere


def test_touches_without_lines():
    assert_that(
        Anywhere("gate-α").touches(FakeLines({})),
        equal_to(True),
        "A place without a file must count as touched",
    )


def test_names_no_file():
    assert_that(
        Anywhere("whole run").properties(), empty(), "A place must name no file"
    )


def test_prints_its_label():
    assert_that(
        str(Anywhere("  spaced  ")),
        equal_to("  spaced  "),
        "A place must print its label",
    )
