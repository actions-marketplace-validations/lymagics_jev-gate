import os

from hamcrest import assert_that, contains_exactly

from jev_gate.diff_sources import DiffSources
from jev_gate.directory import PackDirectory
from jev_gate.git import GitRepository
from jev_gate.paths import Paths
from jev_gate.selection import Selection
from jev_gate.worktree import Worktree
from scratch import Scratch


def packs():
    return PackDirectory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "jev_gate", "packs")
    ).packs()


def test_offers_only_touched_syntax_candidates():
    with Scratch("diff-syntax") as scratch:
        base = scratch.write({"m.py": "class Old:\n    pass\n"}).commit("base")
        scratch.write(
            {"m.py": "class Old:\n    pass\n\n\nclass Added:\n    pass\n"}
        ).commit("x")
        repository = GitRepository(scratch.path)
        assert_that(
            [
                c.name()
                for c in DiffSources(
                    repository,
                    base,
                    Selection(Worktree(repository, scratch.path), Paths(["**"], [])),
                    packs(),
                ).candidates("type")
            ],
            contains_exactly("Added"),
            "Diff mode must offer only candidates with added lines",
        )


def test_offers_changed_hunks():
    with Scratch("diff-hunk") as scratch:
        base = scratch.write({"c.yml": "a: 1\nb: 2\n"}).commit("base")
        scratch.write({"c.yml": "a: 1\nb: 3\n"}).commit("x")
        repository = GitRepository(scratch.path)
        assert_that(
            [
                c.name()
                for c in DiffSources(
                    repository,
                    base,
                    Selection(Worktree(repository, scratch.path), Paths(["**"], [])),
                    packs(),
                ).candidates("hunk")
            ],
            contains_exactly("c.yml"),
            "Diff mode must offer the changed hunk",
        )


def test_offers_commits_after_base():
    with Scratch("diff-commit") as scratch:
        base = scratch.write({"r.md": "1"}).commit("base")
        scratch.write({"r.md": "2"}).commit("Bump the readme")
        repository = GitRepository(scratch.path)
        assert_that(
            [
                c.name()
                for c in DiffSources(
                    repository,
                    base,
                    Selection(Worktree(repository, scratch.path), Paths(["**"], [])),
                    packs(),
                ).candidates("commit")
            ],
            contains_exactly("Bump the readme"),
            "Diff mode must offer each new commit",
        )


def test_offers_changed_tests():
    with Scratch("diff-changed") as scratch:
        base = scratch.write(
            {"t.rs": "#[test]\nfn adds() {\n    assert!(true);\n}\n"}
        ).commit("base")
        scratch.write(
            {"t.rs": "#[test]\nfn adds() {\n    assert!(1 == 1);\n}\n"}
        ).commit("x")
        repository = GitRepository(scratch.path)
        assert_that(
            [
                c.name()
                for c in DiffSources(
                    repository,
                    base,
                    Selection(Worktree(repository, scratch.path), Paths(["**"], [])),
                    packs(),
                ).candidates("changed_test")
            ],
            contains_exactly("adds"),
            "Diff mode must offer the edited test",
        )
