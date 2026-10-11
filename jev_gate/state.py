from jev_gate.contracts import State


class KnownState(State):
    def __init__(self, fields: dict[str, str]):
        self.fields = fields

    def known(self) -> bool:
        return True

    def payload(self) -> dict[str, str]:
        return dict(self.fields)

    def missing(self) -> str:
        raise Exception("A known state misses no field")


class UnknownState(State):
    def __init__(self, field: str):
        self.field = field

    def known(self) -> bool:
        return False

    def payload(self) -> dict[str, str]:
        raise Exception(
            f"The state is unknown because '{self.field}' is not written down"
        )

    def missing(self) -> str:
        return self.field
