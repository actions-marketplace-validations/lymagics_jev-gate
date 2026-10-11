import re

from jev_gate.contracts import Mask


class Glob(Mask):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def matches(self, path: str) -> bool:
        return re.fullmatch(self._regex(), path) is not None

    def _regex(self) -> str:
        parts = re.split(r"(\*\*/|\*\*|\*|\?)", self.pattern)
        tokens = {"**/": "(?:.*/)?", "**": ".*", "*": "[^/]*", "?": "[^/]"}
        return "".join(tokens.get(part, re.escape(part)) for part in parts)
