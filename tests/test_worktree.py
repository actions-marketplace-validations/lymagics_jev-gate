from hamcrest import assert_that, contains_inanyorder, equal_to

from jev_gate.git import GitRepository
from jev_gate.worktree import Worktree
from scratch import Scratch


def test_lists_tracked_files_only():
    with Scratch("worktree-paths") as scratch:
        scratch.write({"kept/a b.py": "", "z.md": ""}).commit("track")
        scratch.write({"untracked.tmp": ""})
        assert_that(
            Worktree(GitRepository(scratch.path), scratch.path).paths(),
            contains_inanyorder("kept/a b.py", "z.md"),
            "Only tracked files must be listed",
        )


def test_reads_current_text_of_a_file():
    with Scratch("worktree-text") as scratch:
        scratch.write({"t.ini": "old"}).commit("old")
        scratch.write({"t.ini": "new ✓"})
        assert_that(
            Worktree(GitRepository(scratch.path), scratch.path).text("t.ini"),
            equal_to("new ✓"),
            "The worktree must read the file on disk",
        )


def test_says_a_missing_file_is_absent():
    with Scratch("worktree-present") as scratch:
        assert_that(
            Worktree(GitRepository(scratch.path), scratch.path).present("nope.txt"),
            equal_to(False),
            "A missing file must be absent",
        )
