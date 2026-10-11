from hamcrest import assert_that, contains_exactly, equal_to

from jev_gate.git import GitRepository
from jev_gate.revision import Revision
from scratch import Scratch


def test_lists_files_of_that_revision():
    with Scratch("revision-paths") as scratch:
        first = scratch.write({"one.c": "1"}).commit("one")
        scratch.write({"two.c": "2"}).commit("two")
        assert_that(
            Revision(GitRepository(scratch.path), first).paths(),
            contains_exactly("one.c"),
            "A revision must list its own files",
        )


def test_reads_text_as_it_was():
    with Scratch("revision-text") as scratch:
        first = scratch.write({"v.txt": "was"}).commit("was")
        scratch.write({"v.txt": "is"}).commit("is")
        assert_that(
            Revision(GitRepository(scratch.path), first).text("v.txt"),
            equal_to("was"),
            "A revision must read old text",
        )


def test_knows_a_file_was_absent():
    with Scratch("revision-present") as scratch:
        first = scratch.write({"a.txt": ""}).commit("a")
        scratch.write({"b.txt": ""}).commit("b")
        assert_that(
            Revision(GitRepository(scratch.path), first).present("b.txt"),
            equal_to(False),
            "A later file must be absent from an earlier revision",
        )
