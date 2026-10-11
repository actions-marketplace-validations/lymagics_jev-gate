from collections.abc import Iterator

from jev_gate.contracts import Candidate, Candidates, Tree
from jev_gate.packs import Packs
from jev_gate.syntax import Syntax


class SyntaxCandidates(Candidates):
    def __init__(self, tree: Tree, packs: Packs, scope: str):
        self.tree = tree
        self.packs = packs
        self.scope = scope

    def __iter__(self) -> Iterator[Candidate]:
        for path in self.tree.paths():
            for pack in self.packs.matching(path, self.scope):
                yield from Syntax(
                    pack.grammar(path),
                    pack.rule(self.scope),
                    path,
                    self.tree.text(path),
                )
