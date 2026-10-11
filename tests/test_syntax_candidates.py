from hamcrest import assert_that, contains_exactly

from fakes import FakeTree
from jev_gate.pack import Pack
from jev_gate.packs import Packs
from jev_gate.syntax_candidates import SyntaxCandidates


def test_reads_only_files_some_pack_covers():
    assert_that(
        [
            str(candidate.place())
            for candidate in SyntaxCandidates(
                FakeTree({"a.py": "class A: pass\n", "b.txt": "class B: pass\n"}),
                Packs(
                    [
                        Pack(
                            "python",
                            {
                                "grammars": {".py": "python"},
                                "scopes": {
                                    "type": {"match": "(class_definition) @candidate"}
                                },
                            },
                        )
                    ]
                ),
                "type",
            )
        ],
        contains_exactly("a.py:1"),
        "Only files read by a pack must give syntax candidates",
    )
