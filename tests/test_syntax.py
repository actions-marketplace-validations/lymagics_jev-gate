from hamcrest import assert_that, calling, contains_exactly, equal_to, raises

from jev_gate.grammar import Grammar
from jev_gate.rule import Rule
from jev_gate.syntax import Syntax


def test_offers_one_candidate_per_matched_node():
    assert_that(
        [
            candidate.name()
            for candidate in Syntax(
                Grammar("python"),
                Rule(
                    "type",
                    {"match": "(class_definition name: (identifier) @name) @candidate"},
                ),
                "m.py",
                "class Ünï:\n    pass\n\nclass Two:\n    pass\n",
            )
        ],
        contains_exactly("Ünï", "Two"),
        "Each matched class must be a candidate",
    )


def test_places_candidates_on_their_lines():
    assert_that(
        [
            str(candidate.place())
            for candidate in Syntax(
                Grammar("python"),
                Rule("type", {"match": "(class_definition) @candidate"}),
                "deep/w.py",
                "\n\n\nclass W:\n    x = 1\n",
            )
        ],
        contains_exactly("deep/w.py:4"),
        "A candidate must start on its first line",
    )


def test_collects_field_captures_inside_the_candidate():
    assert_that(
        next(
            iter(
                Syntax(
                    Grammar("python"),
                    Rule(
                        "test",
                        {
                            "match": "(function_definition name: (identifier) @phrase) @candidate",
                            "fields": {"assertion": "(assert_statement) @assertion"},
                        },
                    ),
                    "t.py",
                    "def test_a():\n    assert 1\n    assert 2\n\nassert 3\n",
                )
            )
        )
        .state(("assertion",))
        .payload(),
        equal_to({"assertion": "assert 1\nassert 2"}),
        "Only captures inside the candidate must join its field",
    )


def test_reads_the_phrase_aloud():
    assert_that(
        next(
            iter(
                Syntax(
                    Grammar("python"),
                    Rule(
                        "test",
                        {
                            "match": "(function_definition name: (identifier) @phrase) @candidate"
                        },
                    ),
                    "p.py",
                    "def test_drops_stale_cache():\n    pass\n",
                )
            )
        )
        .state(("phrase",))
        .payload(),
        equal_to({"phrase": "it drops stale cache"}),
        "A phrase must be read aloud",
    )


def test_fills_unwritten_fields_from_defaults():
    assert_that(
        next(
            iter(
                Syntax(
                    Grammar("rust"),
                    Rule(
                        "function",
                        {
                            "match": "(function_item name: (identifier) @name"
                            " return_type: (_)? @returns) @candidate",
                            "defaults": {"returns": "()"},
                        },
                    ),
                    "l.rs",
                    "fn quiet() {}\n",
                )
            )
        )
        .state(("returns",))
        .payload(),
        equal_to({"returns": "()"}),
        "A missing field must take its default",
    )


def test_names_a_candidate_without_a_name_by_its_first_line():
    assert_that(
        [
            candidate.name()
            for candidate in Syntax(
                Grammar("javascript"),
                Rule("throw", {"match": "(throw_statement) @candidate"}),
                "e.js",
                "function f() {\n  throw new Error(\n    'x');\n}\n",
            )
        ],
        contains_exactly("throw new Error("),
        "A nameless candidate must be named by its first line",
    )


def test_unquotes_quoted_names():
    assert_that(
        [
            candidate.name()
            for candidate in Syntax(
                Grammar("ruby"),
                Rule(
                    "test",
                    {
                        "match": "(call arguments: (argument_list . (string) @phrase)) @candidate"
                    },
                ),
                "s_spec.rb",
                "it 'rejects “smart” quotes' do\nend\n",
            )
        ],
        contains_exactly("rejects “smart” quotes"),
        "A quoted name must lose its quotes",
    )


def test_refuses_a_query_without_candidate_capture():
    assert_that(
        calling(list).with_args(
            Syntax(
                Grammar("python"),
                Rule("odd", {"match": "(identifier) @name"}),
                "o.py",
                "x\n",
            )
        ),
        raises(Exception, "@candidate"),
        "A query without @candidate must fail",
    )
