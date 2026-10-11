import re


class Phrase:
    def __init__(self, raw: str):
        self.raw = raw

    def __str__(self) -> str:
        words = self._words()
        if words[:1] == ["it"]:
            words = words[1:]
        return " ".join(["it", *words])

    def _words(self) -> list[str]:
        quoted = re.fullmatch(r"[A-Za-z@$]*([\"'`])(.*)\1", self.raw.strip(), re.DOTALL)
        words = self._split(quoted.group(2) if quoted else self.raw)
        if not quoted:
            words = self._unprefixed(words)
        return words

    def _split(self, text: str) -> list[str]:
        spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
        return [word.lower() for word in re.split(r"[\s_\-]+", spaced) if word]

    def _unprefixed(self, words: list[str]) -> list[str]:
        if words[:1] in (["test"], ["tests"]):
            words = words[1:]
        if words[-1:] in (["test"], ["tests"]):
            words = words[:-1]
        return words
