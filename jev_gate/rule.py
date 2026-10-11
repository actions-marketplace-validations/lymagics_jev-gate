class Rule:
    def __init__(self, scope: str, data: dict):
        self.kind = scope
        self.data = data

    def scope(self) -> str:
        return self.kind

    def match(self) -> str:
        if "match" not in self.data:
            raise Exception(f"The '{self.kind}' scope has no 'match' query")
        return str(self.data["match"])

    def fields(self) -> dict[str, str]:
        return dict(self.data.get("fields") or {})

    def defaults(self) -> dict[str, str]:
        return {
            key: str(value) for key, value in (self.data.get("defaults") or {}).items()
        }
