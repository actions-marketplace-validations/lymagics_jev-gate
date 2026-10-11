import pytest
from hamcrest import assert_that, calling, equal_to, raises

from jev_gate.state import KnownState, UnknownState


def test_known_state_is_known():
    assert_that(
        KnownState({}).known(), equal_to(True), "A known state must say it is known"
    )


def test_known_state_gives_its_fields():
    assert_that(
        KnownState({"phrase": "it ✓ works", "message": ""}).payload(),
        equal_to({"phrase": "it ✓ works", "message": ""}),
        "A known state must give every field",
    )


def test_known_state_refuses_to_name_a_missing_field():
    assert_that(
        calling(KnownState({"x": "1"}).missing),
        raises(Exception, "misses no field"),
        "A known state must refuse to name a missing field",
    )


def test_unknown_state_is_unknown():
    assert_that(
        UnknownState("returns").known(), equal_to(False), "It must say it is unknown"
    )


def test_unknown_state_names_the_missing_field():
    assert_that(
        UnknownState("returns").missing(),
        equal_to("returns"),
        "An unknown state must name its missing field",
    )


@pytest.mark.parametrize("field", ["returns", "message"])
def test_unknown_state_refuses_a_payload(field: str):
    assert_that(
        calling(UnknownState(field).payload),
        raises(Exception, field),
        "An unknown state must refuse to give a payload",
    )
