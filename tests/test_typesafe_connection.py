import pytest
from hamcrest import assert_that, calling, instance_of, raises

from jev_gate.jev import Jev
from jev_gate.typesafe_connection import TypeSafeConnection


@pytest.mark.parametrize("key", ["", "   "])
def test_refuses_to_work_without_a_key(key: str):
    assert_that(
        calling(TypeSafeConnection(key).model).with_args("jev-1.13.0"),
        raises(Exception, "TYPESAFE_API_KEY"),
        "A missing key must fail before any request",
    )


def test_refuses_a_malformed_key():
    assert_that(
        calling(TypeSafeConnection("key with\ttab").model).with_args("jev-1.13.0"),
        raises(Exception, "rejected"),
        "A malformed key must fail",
    )


def test_gives_a_jev_model():
    assert_that(
        TypeSafeConnection("ts-k3y").model("jev-1.13.0"),
        instance_of(Jev),
        "A connection with a key must give Jev",
    )
