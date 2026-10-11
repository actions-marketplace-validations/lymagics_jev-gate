from jev_gate.contracts import Mask, Tree


class Selection(Tree, Mask):
    def __init__(self, origin: Tree, mask: Mask):
        self.origin = origin
        self.mask = mask

    def paths(self) -> list[str]:
        return [path for path in self.origin.paths() if self.mask.matches(path)]

    def text(self, path: str) -> str:
        return self.origin.text(path)

    def present(self, path: str) -> bool:
        return self.mask.matches(path) and self.origin.present(path)

    def matches(self, path: str) -> bool:
        return self.mask.matches(path)
