import pytest
from hamcrest import assert_that, equal_to

from jev_gate.glob import Glob


@pytest.mark.parametrize(
    "pattern, path",
    [
        ("**", "deep/inside/ünïcode file.py"),
        ("src/**", "src/a/b/c.rs"),
        ("**/generated/**", "generated/x.ts"),
        ("**/generated/**", "lib/generated/y/z.ts"),
        ("*.py", "setup.py"),
        ("tests/test_?.py", "tests/test_7.py"),
        ("docs/[draft].md", "docs/[draft].md"),
    ],
)
def test_matches_paths_it_covers(pattern: str, path: str):
    assert_that(
        Glob(pattern).matches(path), equal_to(True), f"'{pattern}' must match '{path}'"
    )


@pytest.mark.parametrize(
    "pattern, path",
    [
        ("*.py", "pkg/setup.py"),
        ("src/**", "source/main.c"),
        ("tests/test_?.py", "tests/test_42.py"),
        ("docs/[draft].md", "docs/d.md"),
        ("a.b", "aXb"),
    ],
)
def test_rejects_paths_it_does_not_cover(pattern: str, path: str):
    assert_that(
        Glob(pattern).matches(path),
        equal_to(False),
        f"'{pattern}' must not match '{path}'",
    )
