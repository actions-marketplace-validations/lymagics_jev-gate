from collections.abc import Iterator

from jev_gate.candidate import FieldCandidate
from jev_gate.contracts import Candidate, Candidates, Mask, Repository
from jev_gate.listed import Listed
from jev_gate.packs import Packs
from jev_gate.patch import Patch
from jev_gate.revision import Revision
from jev_gate.selection import Selection
from jev_gate.sha import Sha
from jev_gate.syntax_candidates import SyntaxCandidates
from jev_gate.touched import Touched


class Commits(Candidates):
    def __init__(self, repository: Repository, base: str, mask: Mask, packs: Packs):
        self.repository = repository
        self.base = base
        self.mask = mask
        self.packs = packs

    def __iter__(self) -> Iterator[Candidate]:
        log = self.repository.output(
            "log",
            "--reverse",
            "--no-merges",
            "--format=%H%x1f%s%x1f%b%x1e",
            f"{self.base}..HEAD",
        )
        for record in log.split("\x1e"):
            if record.strip("\n"):
                sha, subject, body = record.strip("\n").split("\x1f", 2)
                yield self._candidate(sha, subject, body.strip())

    def _candidate(self, sha: str, subject: str, body: str) -> Candidate:
        patch = Patch(
            self.repository.output(
                "show", "--format=", "--no-color", "--no-ext-diff", "--no-renames", sha
            )
        )
        sections = [
            section for section in patch.sections() if self.mask.matches(section.path())
        ]
        tests = Touched(
            SyntaxCandidates(
                Selection(
                    Revision(self.repository, sha), Listed([s.path() for s in sections])
                ),
                self.packs,
                "test",
            ),
            patch,
        )
        return FieldCandidate(
            "commit",
            subject,
            Sha(sha),
            {
                "subject": subject,
                "message": body,
                "diff": "".join(str(section) for section in sections),
                "tests": "\n".join(
                    test.state(("phrase",)).payload()["phrase"] for test in tests
                ),
            },
        )
