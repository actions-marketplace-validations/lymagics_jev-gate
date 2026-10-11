from jev_gate.contracts import Candidates, Sources, Tree
from jev_gate.files import Files
from jev_gate.packs import Packs
from jev_gate.syntax_candidates import SyntaxCandidates


class FullSources(Sources):
    def __init__(self, tree: Tree, packs: Packs):
        self.tree = tree
        self.packs = packs

    def candidates(self, scope: str) -> Candidates:
        result: Candidates = SyntaxCandidates(self.tree, self.packs, scope)
        if scope == "file":
            result = Files(self.tree)
        return result
