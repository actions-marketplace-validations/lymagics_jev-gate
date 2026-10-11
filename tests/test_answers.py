from hamcrest import assert_that, calling, equal_to, raises

from jev_gate.answers import Oversized, OversizedAnswers, Probabilities, Probability


def test_probability_is_not_oversized():
    assert_that(
        Probability(0.0).oversized(), equal_to(False), "A probability must be judged"
    )


def test_probability_gives_its_value():
    assert_that(
        Probability(0.999).probability(), equal_to(0.999), "It must give its value"
    )


def test_oversized_answer_is_oversized():
    assert_that(
        Oversized("too big").oversized(), equal_to(True), "It must say it is oversized"
    )


def test_oversized_answer_has_no_probability():
    assert_that(
        calling(Oversized("33k tokens").probability),
        raises(Exception, "33k tokens"),
        "An oversized answer must refuse a probability and say why",
    )


def test_probabilities_give_the_named_answer():
    assert_that(
        Probabilities({"g1": 0.2, "g2": 0.8}).answer("g2").probability(),
        equal_to(0.8),
        "The answer must be the one named",
    )


def test_probabilities_refuse_a_missing_answer():
    assert_that(
        calling(Probabilities({}).answer).with_args("ghost-gate"),
        raises(Exception, "ghost-gate"),
        "A missing answer must fail and be named",
    )


def test_oversized_answers_are_all_oversized():
    assert_that(
        OversizedAnswers("limit").answer("any").oversized(),
        equal_to(True),
        "Every answer of an oversized request must be oversized",
    )
