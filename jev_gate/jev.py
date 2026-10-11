import re

import typesafe_sdk

from jev_gate.answers import OversizedAnswers, Probabilities
from jev_gate.contracts import Answers, Model


class Jev(Model):
    def __init__(self, client: typesafe_sdk.TypeSafeClient, version: str):
        self.client = client
        self.version = version

    def answers(self, state: dict[str, str], questions: dict[str, str]) -> Answers:
        try:
            response = self.client.system_one(
                state=state,
                questions={
                    key: typesafe_sdk.Noul(instructions=text)
                    for key, text in questions.items()
                },
                model=self.version,
            )
            result: Answers = Probabilities(
                {key: answer.noul for key, answer in response.nouls.items()}
            )
        except typesafe_sdk.TypeSafeAPIError as e:
            if not self._oversize(e):
                raise Exception(f"Jev rejected the request: {e}") from e
            result = OversizedAnswers(str(e.body))
        except typesafe_sdk.TypeSafeError as e:
            raise Exception(f"Jev could not be reached: {e}") from e
        return result

    def _oversize(self, error: typesafe_sdk.TypeSafeAPIError) -> bool:
        return error.status in (400, 413, 422) and bool(
            re.search(
                r"token|context|too long|too large|length|exceed",
                str(error.body),
                re.IGNORECASE,
            )
        )
