from jev_gate.contracts import Answer, Answers


class Probability(Answer):
    def __init__(self, value: float):
        self.value = value

    def oversized(self) -> bool:
        return False

    def probability(self) -> float:
        return self.value


class Oversized(Answer):
    def __init__(self, reason: str):
        self.reason = reason

    def oversized(self) -> bool:
        return True

    def probability(self) -> float:
        raise Exception(f"An oversized candidate has no probability: {self.reason}")


class Probabilities(Answers):
    def __init__(self, values: dict[str, float]):
        self.values = values

    def answer(self, key: str) -> Answer:
        if key not in self.values:
            raise Exception(f"Jev returned no answer for the '{key}' question")
        return Probability(self.values[key])


class OversizedAnswers(Answers):
    def __init__(self, reason: str):
        self.reason = reason

    def answer(self, key: str) -> Answer:
        return Oversized(self.reason)
