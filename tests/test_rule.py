from hamcrest import assert_that, calling, empty, equal_to, raises

from jev_gate.rule import Rule


def test_gives_its_scope():
    assert_that(
        Rule("catch", {"match": "(x)"}).scope(),
        equal_to("catch"),
        "It must give a scope",
    )


def test_gives_its_match_query():
    assert_that(
        Rule("log", {"match": "(call) @candidate"}).match(),
        equal_to("(call) @candidate"),
        "A rule must give its match query",
    )


def test_refuses_to_work_without_a_match_query():
    assert_that(
        calling(Rule("custom_thing", {"fields": {}}).match),
        raises(Exception, "custom_thing"),
        "A rule without a match query must fail and name its scope",
    )


def test_has_no_field_queries_by_default():
    assert_that(
        Rule("type", {"match": "(a)"}).fields(),
        empty(),
        "Field queries must default empty",
    )


def test_turns_defaults_into_text():
    assert_that(
        Rule("function", {"match": "(f)", "defaults": {"returns": 0}}).defaults(),
        equal_to({"returns": "0"}),
        "Default values must become text",
    )
