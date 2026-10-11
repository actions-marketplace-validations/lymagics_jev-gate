from hamcrest import assert_that, calling, equal_to, raises

from jev_gate.git import GitRepository
from scratch import Scratch


def test_returns_command_output():
    with Scratch("git-output") as scratch:
        scratch.write({"ü.txt": "1"}).commit("first")
        assert_that(
            GitRepository(scratch.path).output("ls-files"),
            equal_to("ü.txt\n"),
            "Git output must come back unquoted",
        )


def test_fails_with_the_error_of_git():
    with Scratch("git-failure") as scratch:
        assert_that(
            calling(GitRepository(scratch.path).output).with_args(
                "show", "no-such-ref-x9"
            ),
            raises(Exception, "no-such-ref-x9"),
            "A failed git command must fail with its arguments",
        )
