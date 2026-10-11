from hamcrest import assert_that, contains_exactly, equal_to

from fakes import FakeTree
from jev_gate.paths import Paths
from jev_gate.selection import Selection


def test_lists_only_chosen_paths():
    assert_that(
        Selection(
            FakeTree({"src/a.rs": "", "target/b.rs": "", "src/gen/c.rs": ""}),
            Paths(["src/**"], ["src/gen/**"]),
        ).paths(),
        contains_exactly("src/a.rs"),
        "A selection must list only chosen paths",
    )


def test_reads_text_from_its_origin():
    assert_that(
        Selection(FakeTree({"t.ex": "defmodule"}), Paths(["**"], [])).text("t.ex"),
        equal_to("defmodule"),
        "A selection must read through to its origin",
    )


def test_hides_present_but_excluded_files():
    assert_that(
        Selection(FakeTree({"x.lock": "{}"}), Paths(["**"], ["*.lock"])).present(
            "x.lock"
        ),
        equal_to(False),
        "An excluded file must not be present",
    )


def test_matches_like_its_mask():
    assert_that(
        Selection(FakeTree({}), Paths(["lib/**"], [])).matches("lib/never/written.py"),
        equal_to(True),
        "A selection must match paths its mask matches, even absent ones",
    )
