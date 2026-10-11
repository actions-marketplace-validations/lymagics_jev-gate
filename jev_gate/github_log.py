from typing import TextIO

from jev_gate.contracts import Log, Place


class GithubLog(Log):
    def __init__(self, stream: TextIO):
        self.stream = stream

    def error(self, place: Place, title: str, text: str):
        self._command("error", place, title, text)

    def warning(self, place: Place, title: str, text: str):
        self._command("warning", place, title, text)

    def info(self, text: str):
        self.stream.write(f"{text}\n")
        self.stream.flush()

    def _command(self, kind: str, place: Place, title: str, text: str):
        properties = ",".join(
            f"{key}={self._property(value)}"
            for key, value in {**place.properties(), "title": title}.items()
        )
        self.stream.write(f"::{kind} {properties}::{self._data(text)}\n")
        self.stream.flush()

    def _data(self, text: str) -> str:
        return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")

    def _property(self, text: str) -> str:
        return self._data(text).replace(":", "%3A").replace(",", "%2C")
