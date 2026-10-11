from jev_gate.contracts import Mask
from jev_gate.glob import Glob


class Paths(Mask):
    def __init__(self, include: list[str], exclude: list[str]):
        self.include = include
        self.exclude = exclude

    def matches(self, path: str) -> bool:
        return any(Glob(glob).matches(path) for glob in self.include) and not any(
            Glob(glob).matches(path) for glob in self.exclude
        )
