from hamcrest import assert_that, calling, equal_to, raises

from jev_gate.pack import Pack


def test_covers_files_by_extension_ignoring_case():
    assert_that(
        Pack("rb", {"grammars": {".rb": "ruby"}}).covers("lib/Task.RB"),
        equal_to(True),
        "A pack must cover its extensions in any case",
    )


def test_ignores_files_without_its_extensions():
    assert_that(
        Pack("rb", {"grammars": {".rb": "ruby"}}).covers("Rakefile"),
        equal_to(False),
        "A pack must not cover a file without its extension",
    )


def test_knows_its_scopes():
    assert_that(
        Pack("p", {"scopes": {"catch": {"match": "(m)"}}}).knows("throw"),
        equal_to(False),
        "A pack must not know a scope it does not define",
    )


def test_gives_a_rule_for_its_scope():
    assert_that(
        Pack("p", {"scopes": {"log": {"match": "(log) @candidate"}}})
        .rule("log")
        .match(),
        equal_to("(log) @candidate"),
        "A pack must give the rule of its scope",
    )


def test_refuses_a_rule_for_an_unknown_scope():
    assert_that(
        calling(Pack("tiny", {"scopes": {}}).rule).with_args("variable"),
        raises(Exception, "tiny"),
        "An unknown scope must fail and name the pack",
    )


def test_shares_one_grammar_among_extensions():
    pack = Pack("cpp", {"grammars": {".cc": "cpp", ".hh": "cpp"}})
    assert_that(
        pack.grammar("a.cc") is pack.grammar("b.hh"),
        equal_to(True),
        "Extensions of one grammar must share it",
    )


def test_refuses_a_grammar_for_a_foreign_file():
    assert_that(
        calling(Pack("go", {"grammars": {".go": "go"}}).grammar).with_args("main.zig"),
        raises(Exception, "main.zig"),
        "A foreign file must fail and be named",
    )


def test_extends_with_new_scopes_without_changing_itself():
    pack = Pack(
        "py", {"grammars": {".py": "python"}, "scopes": {"type": {"match": "(t)"}}}
    )
    pack.extended({"fixture": {"match": "(f)"}})
    assert_that(
        pack.knows("fixture"), equal_to(False), "Extending must not change the original"
    )


def test_extended_pack_knows_new_scopes():
    assert_that(
        Pack("py", {"scopes": {}})
        .extended({"fixture": {"match": "(f)"}})
        .knows("fixture"),
        equal_to(True),
        "An extended pack must know its new scope",
    )
