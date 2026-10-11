import os
from functools import cached_property

from jev_gate.grammar import Grammar
from jev_gate.rule import Rule


class Pack:
    def __init__(self, name: str, data: dict):
        self.label = name
        self.data = data

    def covers(self, path: str) -> bool:
        return self._extension(path) in self._grammars

    def knows(self, scope: str) -> bool:
        return scope in (self.data.get("scopes") or {})

    def rule(self, scope: str) -> Rule:
        if not self.knows(scope):
            raise Exception(
                f"The '{self.label}' pack does not define the '{scope}' scope"
            )
        return Rule(scope, self.data["scopes"][scope])

    def grammar(self, path: str) -> Grammar:
        if not self.covers(path):
            raise Exception(f"The '{self.label}' pack does not read '{path}'")
        return self._grammars[self._extension(path)]

    def extended(self, scopes: dict[str, dict]) -> "Pack":
        return Pack(
            self.label,
            {**self.data, "scopes": {**(self.data.get("scopes") or {}), **scopes}},
        )

    @cached_property
    def _grammars(self) -> dict[str, Grammar]:
        shared: dict[str, Grammar] = {}
        for name in (self.data.get("grammars") or {}).values():
            shared.setdefault(name, Grammar(name))
        return {
            extension.lower(): shared[name]
            for extension, name in (self.data.get("grammars") or {}).items()
        }

    def _extension(self, path: str) -> str:
        return os.path.splitext(path)[1].lower()
