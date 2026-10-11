import re
from functools import cached_property

from jev_gate.contracts import Lines
from jev_gate.section import Section


class Patch(Lines):
    def __init__(self, text: str):
        self.text = text

    def touched(self, path: str, first: int, last: int) -> bool:
        return any(first <= number <= last for number in self._added.get(path, set()))

    def sections(self) -> list[Section]:
        pieces = re.split(r"^(?=diff --git )", self.text, flags=re.MULTILINE)
        return [Section(piece) for piece in pieces if piece.startswith("diff --git ")]

    @cached_property
    def _added(self) -> dict[str, set[int]]:
        added: dict[str, set[int]] = {}
        for section in self.sections():
            for hunk in section.hunks():
                added.setdefault(section.path(), set()).update(hunk.added())
        return added
