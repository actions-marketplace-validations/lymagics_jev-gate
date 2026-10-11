import typesafe_sdk

from jev_gate.contracts import Connection, Model
from jev_gate.jev import Jev


class TypeSafeConnection(Connection):
    def __init__(self, key: str):
        self.key = key

    def model(self, version: str) -> Model:
        if not self.key.strip():
            raise Exception("TYPESAFE_API_KEY is not set, so Jev cannot be asked")
        try:
            client = typesafe_sdk.TypeSafeClient(
                api_key=self.key,
                model=version,
                timeout=60.0,
                retry=typesafe_sdk.RetryPolicy(
                    max_retries=5, backoff_max=20.0, timeout=180.0
                ),
            )
        except typesafe_sdk.TypeSafeError as e:
            raise Exception("The TypeSafe client rejected its settings") from e
        return Jev(client, version)
