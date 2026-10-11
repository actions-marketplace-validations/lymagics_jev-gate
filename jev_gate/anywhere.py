from jev_gate.contracts import Lines, Place


class Anywhere(Place):
    def __init__(self, label: str):
        self.label = label

    def touches(self, lines: Lines) -> bool:
        return True

    def properties(self) -> dict[str, str]:
        return {}

    def __str__(self) -> str:
        return self.label
