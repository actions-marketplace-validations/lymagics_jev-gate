import os

from jev_gate.contracts import Repository, Tree


class Worktree(Tree):
    def __init__(self, repository: Repository, root: str):
        self.repository = repository
        self.root = root

    def paths(self) -> list[str]:
        return [
            path
            for path in self.repository.output("ls-files", "-z").split("\0")
            if path
        ]

    def text(self, path: str) -> str:
        with open(os.path.join(self.root, path), "rb") as stream:
            return stream.read().decode("utf-8", "replace")

    def present(self, path: str) -> bool:
        return os.path.isfile(os.path.join(self.root, path))
