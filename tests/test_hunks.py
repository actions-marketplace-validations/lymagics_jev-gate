from hamcrest import assert_that, contains_exactly, equal_to

from jev_gate.hunks import Hunks
from jev_gate.patch import Patch
from jev_gate.paths import Paths


def test_offers_each_hunk_of_selected_files():
    assert_that(
        [
            str(candidate.place())
            for candidate in Hunks(
                Patch(
                    "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n"
                    "@@ -1 +1 @@\n-a\n+b\n@@ -9 +9,2 @@\n-c\n+d\n+e\n"
                    "diff --git a/doc/x.md b/doc/x.md\n--- a/doc/x.md\n+++ b/doc/x.md\n"
                    "@@ -1 +1 @@\n-x\n+y\n"
                ),
                Paths(["src/**"], []),
            )
        ],
        contains_exactly("src/a.py:1", "src/a.py:9"),
        "Only hunks of selected files must be candidates",
    )


def test_states_both_sides():
    assert_that(
        next(
            iter(
                Hunks(
                    Patch(
                        "diff --git a/h.sql b/h.sql\n--- a/h.sql\n+++ b/h.sql\n"
                        "@@ -2,2 +2,2 @@\n select\n-*\n+id\n"
                    ),
                    Paths(["**"], []),
                )
            )
        )
        .state(("path", "before", "after"))
        .payload(),
        equal_to({"path": "h.sql", "before": "select\n*\n", "after": "select\nid\n"}),
        "A hunk must state its path and both sides",
    )


def test_places_a_deletion_on_the_first_line():
    assert_that(
        next(
            iter(
                Hunks(
                    Patch(
                        "diff --git a/d.txt b/d.txt\n--- a/d.txt\n+++ /dev/null\n"
                        "@@ -1,2 +0,0 @@\n-a\n-b\n"
                    ),
                    Paths(["**"], []),
                )
            )
        )
        .place()
        .properties(),
        equal_to({"file": "d.txt", "line": "1"}),
        "A deleted file's hunk must point at line one",
    )
