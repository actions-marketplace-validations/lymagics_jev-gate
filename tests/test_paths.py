from hamcrest import assert_that, equal_to

from jev_gate.paths import Paths


def test_matches_an_included_path():
    assert_that(
        Paths(["lib/**"], []).matches("lib/κ/λ.rb"),
        equal_to(True),
        "An included path must match",
    )


def test_rejects_an_excluded_path_even_when_included():
    assert_that(
        Paths(["**"], ["**/vendor/**"]).matches("app/vendor/jquery.js"),
        equal_to(False),
        "An exclusion must win over an inclusion",
    )


def test_rejects_everything_without_inclusions():
    assert_that(
        Paths([], []).matches("README"),
        equal_to(False),
        "Nothing must match when nothing is included",
    )
