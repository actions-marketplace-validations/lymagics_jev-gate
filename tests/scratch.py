import os
import shutil
import subprocess
import uuid
from typing import Self


class Scratch:
    def __init__(self, label: str):
        self.path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "tmp",
            f"{label}-{uuid.uuid4().hex[:8]}",
        )

    def __enter__(self) -> Self:
        shutil.rmtree(self.path, ignore_errors=True)
        os.makedirs(self.path)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "scratch@example.invalid")
        self.git("config", "user.name", "Scratch")
        self.git("config", "core.autocrlf", "false")
        return self

    def __exit__(self, *details: object):
        shutil.rmtree(self.path, ignore_errors=True)

    def write(self, files: dict[str, str]) -> "Scratch":
        for name, text in files.items():
            target = os.path.join(self.path, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
        return self

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD").strip()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.path,
            capture_output=True,
            check=True,
            text=True,
            timeout=60,
        ).stdout
