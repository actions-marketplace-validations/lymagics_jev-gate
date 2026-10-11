from hamcrest import assert_that, calling, equal_to, raises

from jev_gate.grammar import Grammar


def test_parses_source_into_a_tree():
    assert_that(
        Grammar("python").tree(b"x = 1\n").root_node.type,
        equal_to("module"),
        "A Python source must parse into a module",
    )


def test_compiles_a_query_once():
    grammar = Grammar("rust")
    assert_that(
        grammar.query("(identifier) @n") is grammar.query("(identifier) @n"),
        equal_to(True),
        "The same query must be compiled once",
    )


def test_refuses_a_broken_query():
    assert_that(
        calling(Grammar("ruby").query).with_args("(nonexistent_node_kind) @x"),
        raises(Exception, "does not compile"),
        "A broken query must fail and name its grammar",
    )


def test_refuses_an_unknown_grammar():
    assert_that(
        calling(Grammar("klingon-script").tree).with_args(b""),
        raises(Exception, "klingon-script"),
        "An unknown grammar must fail and name itself",
    )
