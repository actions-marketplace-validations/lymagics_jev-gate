from hamcrest import assert_that, equal_to

from jev_gate.candidate import FieldCandidate
from jev_gate.span import Span


def test_gives_its_scope():
    assert_that(
        FieldCandidate("throw", "raise", Span("e.py", 1, 1), {}).scope(),
        equal_to("throw"),
        "A candidate must give its scope",
    )


def test_gives_its_name():
    assert_that(
        FieldCandidate("type", "Ωmega", Span("o.java", 2, 8), {"name": "Ωmega"}).name(),
        equal_to("Ωmega"),
        "A candidate must give its name",
    )


def test_gives_its_place():
    assert_that(
        str(FieldCandidate("file", "z.sql", Span("z.sql", 1, 400), {}).place()),
        equal_to("z.sql:1"),
        "A candidate must give its place",
    )


def test_states_only_requested_fields():
    assert_that(
        FieldCandidate(
            "test",
            "t",
            Span("t.rs", 3, 9),
            {"phrase": "it ok", "source": "fn t() {}", "x": "y"},
        )
        .state(("phrase",))
        .payload(),
        equal_to({"phrase": "it ok"}),
        "A candidate must send only the requested fields",
    )


def test_states_unknown_when_a_field_is_not_written_down():
    assert_that(
        FieldCandidate("function", "f", Span("f.js", 1, 2), {"name": "f"})
        .state(("name", "returns"))
        .missing(),
        equal_to("returns"),
        "A candidate must name the field its language does not write down",
    )
