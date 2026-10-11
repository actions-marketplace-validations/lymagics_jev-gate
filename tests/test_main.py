import os
import subprocess
import sys

import pytest
from hamcrest import assert_that, contains_string, equal_to

from scratch import Scratch

pytestmark = pytest.mark.deep

GATES = """model: jev-1.13.0
gates:
  - {id: g, scope: file, state: [text], ask: Is it empty?, fail_above: 0.5}
"""


def run(arguments: list[str], key: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "jev_gate", *arguments],
        capture_output=True,
        check=False,
        text=True,
        timeout=120,
        env={**os.environ, "TYPESAFE_API_KEY": key},
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )


def test_exits_with_two_without_an_api_key():
    with Scratch("main-key") as scratch:
        scratch.write({"g.yml": GATES}).commit("only")
        assert_that(
            run(
                [
                    "--config",
                    os.path.join(scratch.path, "g.yml"),
                    "--mode",
                    "full",
                    "--root",
                    scratch.path,
                ],
                "",
            ).returncode,
            equal_to(2),
            "A missing key must exit with code 2",
        )


def test_explains_the_failure_as_an_annotation():
    with Scratch("main-annotation") as scratch:
        scratch.write({"g.yml": "model: jev-latest\ngates: []\n"}).commit("only")
        assert_that(
            run(
                [
                    "--config",
                    os.path.join(scratch.path, "g.yml"),
                    "--mode",
                    "full",
                    "--root",
                    scratch.path,
                ],
                "k",
            ).stdout,
            contains_string("::error title=jev-gate::"),
            "A failure must print one error annotation with its reasons",
        )
