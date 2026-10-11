from functools import cached_property

from jev_gate.changed_tests import ChangedTests
from jev_gate.commits import Commits
from jev_gate.contracts import Candidates, Repository, Sources
from jev_gate.full_sources import FullSources
from jev_gate.hunks import Hunks
from jev_gate.packs import Packs
from jev_gate.patch import Patch
from jev_gate.revision import Revision
from jev_gate.selection import Selection
from jev_gate.touched import Touched


class DiffSources(Sources):
    def __init__(
        self, repository: Repository, base: str, tree: Selection, packs: Packs
    ):
        self.repository = repository
        self.base = base
        self.tree = tree
        self.packs = packs

    def candidates(self, scope: str) -> Candidates:
        special = {
            "hunk": lambda: Hunks(self._patch, self.tree),
            "commit": lambda: Commits(
                self.repository, self.base, self.tree, self.packs
            ),
            "changed_test": lambda: ChangedTests(
                Selection(Revision(self.repository, self.base), self.tree),
                self.tree,
                self.packs,
                self._patch,
            ),
        }
        return special.get(
            scope,
            lambda: Touched(
                FullSources(self.tree, self.packs).candidates(scope), self._patch
            ),
        )()

    @cached_property
    def _patch(self) -> Patch:
        return Patch(
            self.repository.output(
                "diff",
                "--no-color",
                "--no-ext-diff",
                "--no-renames",
                "-U3",
                self.base,
                "--",
            )
        )
