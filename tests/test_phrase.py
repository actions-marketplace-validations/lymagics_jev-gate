import pytest
from hamcrest import assert_that, equal_to
from hypothesis import given
from hypothesis import strategies as st

from jev_gate.phrase import Phrase


@pytest.mark.parametrize(
    "raw, spoken",
    [
        ("test_keeps_headers_of_origin", "it keeps headers of origin"),
        ("keepsHeadersOfOrigin", "it keeps headers of origin"),
        ('"keeps headers of origin"', "it keeps headers of origin"),
        ("'it rejects  blank input'", "it rejects blank input"),
        ("`parses ${kind} rows`", "it parses ${kind} rows"),
        ("KeepsHeaders_WhenOriginIsSet", "it keeps headers when origin is set"),
        ("parsesHTTPServerName", "it parses http server name"),
        ("rendersPage42Fast", "it renders page42 fast"),
        ("closesStreamTest", "it closes stream"),
        ("test", "it"),
        ("TestCaseDropsTail", "it case drops tail"),
    ],
)
def test_reads_names_aloud(raw: str, spoken: str):
    assert_that(str(Phrase(raw)), equal_to(spoken), f"'{raw}' must read as '{spoken}'")


@given(st.text(alphabet=st.characters(categories=["L", "N"]), min_size=1, max_size=30))
def test_always_starts_with_it(raw: str):
    assert_that(
        str(Phrase(raw)).split(" ")[0], equal_to("it"), f"'{raw}' must start with it"
    )
