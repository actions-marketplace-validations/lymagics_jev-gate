from collections.abc import Iterator

from jev_gate.contracts import Candidate, Candidates, Lines


class Touched(Candidates):
    def __init__(self, origin: Candidates, lines: Lines):
        self.origin = origin
        self.lines = lines

    def __iter__(self) -> Iterator[Candidate]:
        return (
            candidate
            for candidate in self.origin
            if candidate.place().touches(self.lines)
        )
