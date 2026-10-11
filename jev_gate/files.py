from collections.abc import Iterator

from jev_gate.candidate import FieldCandidate
from jev_gate.contracts import Candidate, Candidates, Tree
from jev_gate.span import Span


class Files(Candidates):
    def __init__(self, tree: Tree):
        self.tree = tree

    def __iter__(self) -> Iterator[Candidate]:
        for path in self.tree.paths():
            text = self.tree.text(path)
            if "\0" not in text:
                yield FieldCandidate(
                    "file",
                    path,
                    Span(path, 1, max(1, len(text.splitlines()))),
                    {"path": path, "text": text},
                )
