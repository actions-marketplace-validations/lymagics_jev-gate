from collections.abc import Iterator

from jev_gate.answers import OversizedAnswers, Probabilities
from jev_gate.contracts import (
    Answers,
    Candidate,
    Candidates,
    Connection,
    Lines,
    Log,
    Model,
    Place,
    Repository,
    Tree,
)


class FakeRepository(Repository):
    def __init__(self, outputs: dict[tuple[str, ...], str]):
        self.outputs = outputs

    def output(self, *args: str) -> str:
        if args not in self.outputs:
            raise Exception(f"The fake repository knows no output for {args}")
        return self.outputs[args]


class FakeTree(Tree):
    def __init__(self, files: dict[str, str]):
        self.files = files

    def paths(self) -> list[str]:
        return list(self.files)

    def text(self, path: str) -> str:
        return self.files[path]

    def present(self, path: str) -> bool:
        return path in self.files


class FakeLines(Lines):
    def __init__(self, added: dict[str, set[int]]):
        self.added = added

    def touched(self, path: str, first: int, last: int) -> bool:
        return any(first <= number <= last for number in self.added.get(path, set()))


class FakeCandidates(Candidates):
    def __init__(self, items: list[Candidate]):
        self.items = items

    def __iter__(self) -> Iterator[Candidate]:
        return iter(self.items)


class FakeModel(Model):
    def __init__(self, probabilities: dict[str, float]):
        self.probabilities = probabilities

    def answers(self, state: dict[str, str], questions: dict[str, str]) -> Answers:
        return Probabilities({key: self.probabilities[key] for key in questions})


class EchoModel(Model):
    def __init__(self, scale: float):
        self.scale = scale

    def answers(self, state: dict[str, str], questions: dict[str, str]) -> Answers:
        return Probabilities(
            {key: len(questions) * len(state) * self.scale for key in questions}
        )


class OversizedModel(Model):
    def __init__(self, reason: str):
        self.reason = reason

    def answers(self, state: dict[str, str], questions: dict[str, str]) -> Answers:
        return OversizedAnswers(self.reason)


class BrokenModel(Model):
    def __init__(self, reason: str):
        self.reason = reason

    def answers(self, state: dict[str, str], questions: dict[str, str]) -> Answers:
        raise Exception(self.reason)


class FakeConnection(Connection):
    def __init__(self, model: Model):
        self.origin = model

    def model(self, version: str) -> Model:
        return self.origin


class FakeLog(Log):
    def __init__(self):
        self.lines: list[str] = []

    def error(self, place: Place, title: str, text: str):
        self.lines.append(f"error {place.properties()} {title}: {text}")

    def warning(self, place: Place, title: str, text: str):
        self.lines.append(f"warning {place.properties()} {title}: {text}")

    def info(self, text: str):
        self.lines.append(f"info {text}")
