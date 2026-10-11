import os

import yaml

from jev_gate.pack import Pack
from jev_gate.packs import Packs


class PackDirectory:
    def __init__(self, path: str):
        self.path = path

    def packs(self) -> Packs:
        return Packs(
            [
                Pack(os.path.splitext(name)[0], self._data(name))
                for name in sorted(os.listdir(self.path))
                if name.endswith(".yml")
            ]
        )

    def _data(self, name: str) -> dict:
        with open(os.path.join(self.path, name), encoding="utf-8") as stream:
            return yaml.safe_load(stream)
