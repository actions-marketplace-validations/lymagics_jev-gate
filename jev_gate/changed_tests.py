from collections.abc import Iterator

from jev_gate.candidate import FieldCandidate
from jev_gate.contracts import Candidate, Candidates, Lines, Tree
from jev_gate.listed import Listed
from jev_gate.packs import Packs
from jev_gate.selection import Selection
from jev_gate.syntax_candidates import SyntaxCandidates
from jev_gate.touched import Touched


class ChangedTests(Candidates):
    def __init__(self, before: Tree, after: Tree, packs: Packs, lines: Lines):
        self.before = before
        self.after = after
        self.packs = packs
        self.lines = lines

    def __iter__(self) -> Iterator[Candidate]:
        edited = list(
            Touched(SyntaxCandidates(self.after, self.packs, "test"), self.lines)
        )
        paths = sorted({test.place().properties()["file"] for test in edited})
        previous = {
            (test.place().properties()["file"], test.name()): self._source(test)
            for test in SyntaxCandidates(
                Selection(
                    self.before, Listed([p for p in paths if self.before.present(p)])
                ),
                self.packs,
                "test",
            )
        }
        for test in edited:
            key = (test.place().properties()["file"], test.name())
            if key in previous and previous[key] != self._source(test):
                yield FieldCandidate(
                    "changed_test",
                    test.name(),
                    test.place(),
                    {"before": previous[key], "after": self._source(test)},
                )

    def _source(self, test: Candidate) -> str:
        return test.state(("source",)).payload()["source"]
