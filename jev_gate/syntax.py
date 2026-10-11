import re
from collections.abc import Iterator

import tree_sitter

from jev_gate.candidate import FieldCandidate
from jev_gate.contracts import Candidate, Candidates
from jev_gate.grammar import Grammar
from jev_gate.phrase import Phrase
from jev_gate.rule import Rule
from jev_gate.span import Span


class Syntax(Candidates):
    def __init__(self, grammar: Grammar, rule: Rule, path: str, text: str):
        self.grammar = grammar
        self.rule = rule
        self.path = path
        self.text = text

    def __iter__(self) -> Iterator[Candidate]:
        data = self.text.encode("utf-8")
        root = self.grammar.tree(data).root_node
        found: dict[tuple[int, int], tuple[tuple[int, int], dict[str, list[str]]]] = {}
        for _, captures in tree_sitter.QueryCursor(
            self.grammar.query(self.rule.match())
        ).matches(root):
            nodes = captures.get("candidate", [])
            if not nodes:
                raise Exception(
                    f"The '{self.rule.scope()}' query captures no @candidate"
                )
            key = (min(n.start_byte for n in nodes), max(n.end_byte for n in nodes))
            rows = (
                min(n.start_point.row for n in nodes),
                max(n.end_point.row for n in nodes),
            )
            self._absorb(found.setdefault(key, (rows, {}))[1], captures, data, key)
        for key, (rows, fields) in found.items():
            self._extend(fields, root, data, key)
            yield self._candidate(
                fields, data[key[0] : key[1]].decode("utf-8", "replace"), rows
            )

    def _extend(
        self,
        fields: dict[str, list[str]],
        root: tree_sitter.Node,
        data: bytes,
        key: tuple[int, int],
    ):
        for source in self.rule.fields().values():
            cursor = tree_sitter.QueryCursor(self.grammar.query(source))
            cursor.set_byte_range(*key)
            for _, captures in cursor.matches(root):
                self._absorb(fields, captures, data, key)

    def _absorb(
        self,
        fields: dict[str, list[str]],
        captures: dict[str, list[tree_sitter.Node]],
        data: bytes,
        key: tuple[int, int],
    ):
        for name, nodes in captures.items():
            inside = [
                n for n in nodes if key[0] <= n.start_byte and n.end_byte <= key[1]
            ]
            if name != "candidate" and not name.startswith("_") and inside:
                value = data[
                    min(n.start_byte for n in inside) : max(n.end_byte for n in inside)
                ].decode("utf-8", "replace")
                if value not in fields.setdefault(name, []):
                    fields[name].append(value)

    def _candidate(
        self, raw: dict[str, list[str]], text: str, rows: tuple[int, int]
    ) -> Candidate:
        fields = {
            **self.rule.defaults(),
            **{key: "\n".join(values) for key, values in raw.items()},
        }
        if "phrase" in fields:
            fields["phrase"] = "\n".join(str(Phrase(value)) for value in raw["phrase"])
        name = (
            raw.get("name")
            or raw.get("phrase")
            or (text.strip().splitlines() or [text])[:1]
        )[0]
        return FieldCandidate(
            self.rule.scope(),
            re.sub(r"^([\"'`])(.*)\1$", r"\2", name, flags=re.DOTALL),
            Span(self.path, rows[0] + 1, rows[1] + 1),
            fields,
        )
