from jev_gate.contracts import Repository, Tree


class Revision(Tree):
    def __init__(self, repository: Repository, sha: str):
        self.repository = repository
        self.sha = sha

    def paths(self) -> list[str]:
        return self._listing()

    def text(self, path: str) -> str:
        return self.repository.output("show", f"{self.sha}:{path}")

    def present(self, path: str) -> bool:
        return path in self._listing("--", path)

    def _listing(self, *pathspec: str) -> list[str]:
        listing = self.repository.output(
            "ls-tree", "-r", "-z", "--name-only", self.sha, *pathspec
        )
        return [path for path in listing.split("\0") if path]
