import json

import httpx2
import typesafe_sdk
from hamcrest import assert_that, calling, close_to, equal_to, raises

from jev_gate.jev import Jev


class FakeTransport(httpx2.BaseTransport):
    def __init__(self, status: int, body: dict):
        self.status = status
        self.body = body

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(self.status, json=self.body)


class EchoTransport(httpx2.BaseTransport):
    def __init__(self, probability: float):
        self.probability = probability

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        sent = json.loads(request.content)
        return httpx2.Response(
            200,
            json={
                "model": sent["model"],
                "answers": {
                    key: {
                        "type": "noul",
                        "noul": self.probability if "λ" in sent["state"]["x"] else 0,
                    }
                    for key, question in sent["questions"].items()
                    if question == {"type": "noul", "instructions": "Is `x` odd?"}
                },
                "usage": {"input_tokens": 3, "output_tokens": 0},
            },
        )


def client(transport: httpx2.BaseTransport) -> typesafe_sdk.TypeSafeClient:
    return typesafe_sdk.TypeSafeClient(
        api_key="test-key",
        transport=transport,
        retry=typesafe_sdk.RetryPolicy(max_retries=0),
    )


def test_sends_state_and_noul_questions():
    assert_that(
        Jev(client(EchoTransport(0.66)), "jev-1.13.0")
        .answers({"x": "λ-calculus"}, {"odd-gate": "Is `x` odd?"})
        .answer("odd-gate")
        .probability(),
        close_to(0.66, 1e-9),
        "The state and the question must reach Jev as a noul",
    )


def test_reads_noul_probabilities():
    assert_that(
        Jev(
            client(
                FakeTransport(
                    200,
                    {
                        "model": "jev-1.13.0",
                        "answers": {"a": {"type": "noul", "noul": 0.125}},
                        "usage": {"input_tokens": 9, "output_tokens": 0},
                    },
                )
            ),
            "jev-1.13.0",
        )
        .answers({"s": "t"}, {"a": "?"})
        .answer("a")
        .probability(),
        equal_to(0.125),
        "The noul value must be the probability",
    )


def test_treats_a_context_rejection_as_oversized():
    assert_that(
        Jev(
            client(
                FakeTransport(
                    422, {"detail": "state exceeds the context window of 32k tokens"}
                )
            ),
            "jev-1.13.0",
        )
        .answers({"s": "huge"}, {"g": "?"})
        .answer("g")
        .oversized(),
        equal_to(True),
        "A rejection about context length must mean oversized",
    )


def test_fails_on_other_rejections():
    assert_that(
        calling(
            Jev(
                client(FakeTransport(422, {"detail": "questions.g.type is invalid"})),
                "jev-1.13.0",
            ).answers
        ).with_args({"s": "t"}, {"g": "?"}),
        raises(Exception, "rejected"),
        "A malformed request must fail the run",
    )


def test_fails_when_unauthorized():
    assert_that(
        calling(
            Jev(client(FakeTransport(401, {"detail": "bad key"})), "jev-1.13.0").answers
        ).with_args({"s": "t"}, {"g": "?"}),
        raises(Exception, "rejected"),
        "A bad key must fail the run",
    )


def test_fails_when_unreachable():
    assert_that(
        calling(
            Jev(client(FakeTransport(503, {"detail": "down"})), "jev-1.13.0").answers
        ).with_args({"s": "t"}, {"g": "?"}),
        raises(Exception),
        "An unreachable API must fail the run",
    )


class SilentTransport(httpx2.BaseTransport):
    def __init__(self, host: str):
        self.host = host

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError(f"{self.host} is unreachable", request=request)


def test_fails_when_the_network_is_down():
    assert_that(
        calling(
            Jev(client(SilentTransport("api.typesafe.ai")), "jev-1.13.0").answers
        ).with_args({"s": "t"}, {"g": "?"}),
        raises(Exception, "could not be reached"),
        "A dead network must fail the run",
    )
