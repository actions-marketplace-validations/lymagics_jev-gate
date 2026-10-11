from jev_gate.pack import Pack


class Packs:
    def __init__(self, items: list[Pack]):
        self.items = items

    def matching(self, path: str, scope: str) -> list[Pack]:
        return [item for item in self.items if item.covers(path) and item.knows(scope)][
            :1
        ]

    def extended(self, scopes: dict[str, dict[str, dict]]) -> "Packs":
        unknown = set(scopes) - {item.label for item in self.items}
        if unknown:
            raise Exception(f"No language pack is named {', '.join(sorted(unknown))}")
        return Packs([item.extended(scopes.get(item.label, {})) for item in self.items])
