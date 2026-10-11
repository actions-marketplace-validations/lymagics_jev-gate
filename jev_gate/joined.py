from collections.abc import Iterator
from itertools import chain

from jev_gate.contracts import Candidate, Candidates


class Joined(Candidates):
    def __init__(self, parts: list[Candidates]):
        self.parts = parts

    def __iter__(self) -> Iterator[Candidate]:
        return chain.from_iterable(self.parts)
