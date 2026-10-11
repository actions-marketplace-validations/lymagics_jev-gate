from jev_gate.contracts import Lines, Place


class Span(Place):
    def __init__(self, path: str, first: int, last: int):
        self.path = path
        self.first = first
        self.last = last

    def touches(self, lines: Lines) -> bool:
        return lines.touched(self.path, self.first, self.last)

    def properties(self) -> dict[str, str]:
        return {"file": self.path, "line": str(self.first)}

    def __str__(self) -> str:
        return f"{self.path}:{self.first}"
