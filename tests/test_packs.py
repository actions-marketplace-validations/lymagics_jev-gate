from hamcrest import assert_that, calling, contains_exactly, empty, raises

from jev_gate.pack import Pack
from jev_gate.packs import Packs


def test_picks_the_pack_that_reads_the_file_and_scope():
    assert_that(
        [
            pack.label
            for pack in Packs(
                [
                    Pack(
                        "js",
                        {"grammars": {".js": "javascript"}, "scopes": {"test": {}}},
                    ),
                    Pack(
                        "ts",
                        {"grammars": {".ts": "typescript"}, "scopes": {"test": {}}},
                    ),
                ]
            ).matching("spec/a.ts", "test")
        ],
        contains_exactly("ts"),
        "The pack reading the extension must be picked",
    )


def test_picks_nothing_for_an_unknown_scope():
    assert_that(
        Packs([Pack("js", {"grammars": {".js": "javascript"}, "scopes": {}})]).matching(
            "a.js", "log"
        ),
        empty(),
        "No pack must be picked when none defines the scope",
    )


def test_extends_named_packs():
    assert_that(
        [
            pack.knows("story")
            for pack in Packs([Pack("rb", {"scopes": {}}), Pack("cs", {"scopes": {}})])
            .extended({"rb": {"story": {"match": "(s)"}}})
            .items
        ],
        contains_exactly(True, False),
        "Only the named pack must learn the new scope",
    )


def test_refuses_to_extend_an_unknown_pack():
    assert_that(
        calling(Packs([Pack("rb", {})]).extended).with_args({"cobol": {}}),
        raises(Exception, "cobol"),
        "An unknown pack must fail and be named",
    )
