from jev_gate.contracts import Mask


class Listed(Mask):
    def __init__(self, names: list[str]):
        self.names = names

    def matches(self, path: str) -> bool:
        return path in self.names
