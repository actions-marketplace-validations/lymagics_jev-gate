from jev_gate.contracts import Lines, Place


class Sha(Place):
    def __init__(self, digest: str):
        self.digest = digest

    def touches(self, lines: Lines) -> bool:
        return True

    def properties(self) -> dict[str, str]:
        return {}

    def __str__(self) -> str:
        return f"commit {self.digest[:12]}"
