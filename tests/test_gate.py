from hamcrest import assert_that, equal_to, instance_of

from jev_gate.answers import Oversized, Probability
from jev_gate.candidate import FieldCandidate
from jev_gate.gate import YamlGate
from jev_gate.span import Span
from jev_gate.verdicts import Blocked, Fired, Passed, Skipped


def test_gives_its_id():
    assert_that(
        YamlGate({"id": "τ-gate"}, "fail").name(),
        equal_to("τ-gate"),
        "A gate must give its id",
    )


def test_admits_candidates_of_its_scope():
    assert_that(
        YamlGate({"scope": "type"}, "fail").admits(
            FieldCandidate("type", "Bus", Span("b.rs", 1, 1), {})
        ),
        equal_to(True),
        "A gate must admit candidates of its scope",
    )


def test_refuses_candidates_of_other_scopes():
    assert_that(
        YamlGate({"scope": "type"}, "fail").admits(
            FieldCandidate("function", "Bus", Span("b.rs", 1, 1), {})
        ),
        equal_to(False),
        "A gate must refuse candidates of other scopes",
    )


def test_refuses_allowed_names():
    assert_that(
        YamlGate({"scope": "type", "allow": ["Computer", "User"]}, "fail").admits(
            FieldCandidate("type", "Computer", Span("c.java", 3, 30), {})
        ),
        equal_to(False),
        "A gate must never judge an allowed name",
    )


def test_gives_its_state_fields():
    assert_that(
        YamlGate({"state": ["phrase", "message"]}, "fail").fields(),
        equal_to(("phrase", "message")),
        "A gate must give its state fields",
    )


def test_gives_its_question():
    assert_that(
        YamlGate({"ask": "Is `name` a verb?"}, "fail").question(),
        equal_to("Is `name` a verb?"),
        "A gate must give its question",
    )


def test_fires_above_its_threshold():
    assert_that(
        YamlGate({"id": "g", "fail_above": 0.9}, "fail").verdict(
            FieldCandidate("type", "X", Span("x.ts", 1, 1), {}), Probability(0.9001)
        ),
        instance_of(Fired),
        "A probability above the threshold must fire",
    )


def test_passes_at_its_threshold():
    assert_that(
        YamlGate({"id": "g", "fail_above": 0.5}, "fail").verdict(
            FieldCandidate("type", "X", Span("x.ts", 1, 1), {}), Probability(0.5)
        ),
        instance_of(Passed),
        "A probability equal to the threshold must pass",
    )


def test_skips_oversized_candidates_when_told_to():
    assert_that(
        YamlGate({"id": "g", "fail_above": 0.5}, "skip").verdict(
            FieldCandidate("hunk", "h", Span("h", 1, 1), {}), Oversized("big")
        ),
        instance_of(Skipped),
        "The file setting must skip oversized candidates",
    )


def test_blocks_oversized_candidates_by_its_own_setting():
    assert_that(
        YamlGate({"id": "g", "fail_above": 0.5, "oversize": "fail"}, "skip").verdict(
            FieldCandidate("file", "f", Span("f", 1, 1), {}), Oversized("big")
        ),
        instance_of(Blocked),
        "A gate's own setting must override the file's",
    )
