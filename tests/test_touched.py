from hamcrest import assert_that, contains_exactly

from fakes import FakeCandidates, FakeLines
from jev_gate.candidate import FieldCandidate
from jev_gate.span import Span
from jev_gate.touched import Touched


def test_keeps_only_touched_candidates():
    assert_that(
        [
            candidate.name()
            for candidate in Touched(
                FakeCandidates(
                    [
                        FieldCandidate("type", "Early", Span("m.kt", 1, 5), {}),
                        FieldCandidate("type", "Late", Span("m.kt", 30, 31), {}),
                    ]
                ),
                FakeLines({"m.kt": {31}}),
            )
        ],
        contains_exactly("Late"),
        "Only candidates with an added line must stay",
    )
