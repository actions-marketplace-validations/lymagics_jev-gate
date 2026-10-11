import os

from hamcrest import assert_that, contains_exactly, contains_string, equal_to, is_not

from jev_gate.commits import Commits
from jev_gate.directory import PackDirectory
from jev_gate.git import GitRepository
from jev_gate.paths import Paths
from scratch import Scratch


def packs():
    return PackDirectory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "jev_gate", "packs")
    ).packs()


def test_offers_one_candidate_per_commit_after_base():
    with Scratch("commits-each") as scratch:
        base = scratch.write({"a.txt": "a"}).commit("base")
        scratch.write({"b.txt": "b"}).commit("Add b")
        scratch.write({"c.txt": "c"}).commit("Add c")
        assert_that(
            [
                c.name()
                for c in Commits(
                    GitRepository(scratch.path), base, Paths(["**"], []), packs()
                )
            ],
            contains_exactly("Add b", "Add c"),
            "Each commit after the base must be a candidate, oldest first",
        )


def test_states_the_body_as_message():
    with Scratch("commits-body") as scratch:
        base = scratch.write({"a.txt": "a"}).commit("base")
        scratch.write({"b.txt": "b"}).commit(
            "Fix the thing\n\nBecause it was ┌broken┐.\n"
        )
        assert_that(
            next(
                iter(
                    Commits(
                        GitRepository(scratch.path), base, Paths(["**"], []), packs()
                    )
                )
            )
            .state(("message",))
            .payload(),
            equal_to({"message": "Because it was ┌broken┐."}),
            "The commit body must be the message",
        )


def test_keeps_only_selected_files_in_the_diff():
    with Scratch("commits-diff") as scratch:
        base = scratch.write({"src/a.py": "a\n"}).commit("base")
        scratch.write({"src/a.py": "b\n", "vendor/v.js": "v\n"}).commit("Change both")
        assert_that(
            next(
                iter(
                    Commits(
                        GitRepository(scratch.path),
                        base,
                        Paths(["src/**"], []),
                        packs(),
                    )
                )
            )
            .state(("diff",))
            .payload()["diff"],
            is_not(contains_string("vendor/v.js")),
            "Excluded files must not reach the commit diff",
        )


def test_lists_phrases_of_tests_the_commit_touches():
    with Scratch("commits-tests") as scratch:
        base = scratch.write(
            {"t/test_x.py": "def test_old_one():\n    assert True\n"}
        ).commit("base")
        scratch.write(
            {
                "t/test_x.py": "def test_old_one():\n    assert True\n\n\n"
                "def test_rejects_empty_names():\n    assert False\n"
            }
        ).commit("Add a test")
        assert_that(
            next(
                iter(
                    Commits(
                        GitRepository(scratch.path), base, Paths(["**"], []), packs()
                    )
                )
            )
            .state(("tests",))
            .payload(),
            equal_to({"tests": "it rejects empty names"}),
            "Only tests the commit adds or edits must be listed",
        )
