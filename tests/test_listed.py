import pytest
from hamcrest import assert_that, equal_to

from jev_gate.listed import Listed


@pytest.mark.parametrize(
    "path, chosen", [("a/b.c", True), ("a/b.cc", False), ("A/B.C", False)]
)
def test_matches_listed_names_exactly(path: str, chosen: bool):
    assert_that(
        Listed(["a/b.c", "z"]).matches(path),
        equal_to(chosen),
        f"'{path}' must be matched only by its exact name",
    )
