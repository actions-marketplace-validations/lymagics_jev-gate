from hamcrest import assert_that, contains_exactly

from fakes import FakeCandidates
from jev_gate.candidate import FieldCandidate
from jev_gate.joined import Joined
from jev_gate.span import Span


def test_chains_all_parts_in_order():
    assert_that(
        [
            candidate.name()
            for candidate in Joined(
                [
                    FakeCandidates(
                        [FieldCandidate("log", "first", Span("1", 1, 1), {})]
                    ),
                    FakeCandidates([]),
                    FakeCandidates(
                        [FieldCandidate("log", "second", Span("2", 2, 2), {})]
                    ),
                ]
            )
        ],
        contains_exactly("first", "second"),
        "Joined candidates must keep the order of their parts",
    )
