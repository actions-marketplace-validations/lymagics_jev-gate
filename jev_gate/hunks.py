from collections.abc import Iterator

from jev_gate.candidate import FieldCandidate
from jev_gate.contracts import Candidate, Candidates, Mask
from jev_gate.patch import Patch
from jev_gate.span import Span


class Hunks(Candidates):
    def __init__(self, patch: Patch, mask: Mask):
        self.patch = patch
        self.mask = mask

    def __iter__(self) -> Iterator[Candidate]:
        for section in self.patch.sections():
            if self.mask.matches(section.path()):
                for hunk in section.hunks():
                    first = max(1, hunk.line())
                    yield FieldCandidate(
                        "hunk",
                        section.path(),
                        Span(
                            section.path(),
                            first,
                            first + max(0, len(hunk.after().splitlines()) - 1),
                        ),
                        {
                            "path": section.path(),
                            "before": hunk.before(),
                            "after": hunk.after(),
                        },
                    )
