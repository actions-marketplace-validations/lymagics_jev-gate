import os

from hamcrest import assert_that, contains_exactly

from fakes import FakeTree
from jev_gate.directory import PackDirectory
from jev_gate.full_sources import FullSources


def packs():
    return PackDirectory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "jev_gate", "packs")
    ).packs()


def test_offers_every_file_for_file_scope():
    assert_that(
        [
            c.name()
            for c in FullSources(
                FakeTree({"main.tf": "x", "q.sql": "y"}), packs()
            ).candidates("file")
        ],
        contains_exactly("main.tf", "q.sql"),
        "File scope must offer every file",
    )


def test_offers_syntax_candidates_for_other_scopes():
    assert_that(
        [
            c.name()
            for c in FullSources(
                FakeTree({"k.py": "class Kettle:\n    pass\n", "n.md": "class Not"}),
                packs(),
            ).candidates("type")
        ],
        contains_exactly("Kettle"),
        "A syntax scope must offer what its pack finds",
    )
