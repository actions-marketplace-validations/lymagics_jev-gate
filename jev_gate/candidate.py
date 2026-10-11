from jev_gate.contracts import Candidate, Place, State
from jev_gate.state import KnownState, UnknownState


class FieldCandidate(Candidate):
    def __init__(self, scope: str, name: str, place: Place, fields: dict[str, str]):
        self.kind = scope
        self.label = name
        self.spot = place
        self.fields = fields

    def scope(self) -> str:
        return self.kind

    def name(self) -> str:
        return self.label

    def place(self) -> Place:
        return self.spot

    def state(self, fields: tuple[str, ...]) -> State:
        absent = [field for field in fields if field not in self.fields]
        result: State = (
            UnknownState(absent[0])
            if absent
            else KnownState({field: self.fields[field] for field in fields})
        )
        return result
