import subprocess

from jev_gate.contracts import Repository


class GitRepository(Repository):
    def __init__(self, root: str):
        self.root = root

    def output(self, *args: str) -> str:
        try:
            done = subprocess.run(
                ["git", "-c", "core.quotepath=off", *args],
                cwd=self.root,
                capture_output=True,
                timeout=300,
                check=False,
            )
        except subprocess.TimeoutExpired as e:
            raise Exception(
                f"git {' '.join(args)} did not finish in 300 seconds"
            ) from e
        if done.returncode != 0:
            raise Exception(
                f"git {' '.join(args)} failed with code {done.returncode}: "
                f"{done.stderr.decode('utf-8', 'replace').strip()}"
            )
        return done.stdout.decode("utf-8", "replace")
