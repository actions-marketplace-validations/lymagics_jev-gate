import os

import pytest
from hamcrest import assert_that, contains_exactly, equal_to

from fakes import FakeTree
from jev_gate.directory import PackDirectory
from jev_gate.syntax_candidates import SyntaxCandidates

PYTHON = """import logging
class Vault(Base):
    def open(self, code: int) -> bool:
        tries = 1
        try:
            raise ValueError("code is wrong")
        except KeyError as err:
            logging.warning("lost %s", err)
        return True
    def _hidden(self):
        pass
def test_keeps_headers_of_origin():
    assert 1 == 2, "headers were dropped"
    assert_that(a, equal_to(b), "origin differs")
"""

JAVASCRIPT = """class Vault { open(code) { let tries = 1;
  try { throw new Error("code is wrong"); }
  catch (err) { console.warn("lost", err); } } }
function close(force) { return force; }
it("keeps headers of origin", () => { expect(a).toBe(1); assert.equal(a, b, "origin differs"); });
promise.catch(() => {});
"""

TYPESCRIPT = """interface Door { open(): boolean; }
class Vault implements Door { public open(): boolean { return true; }
  private spin(n: number): void {} }
export function close(force: boolean): string { const tries: number = 2; return ""; }
test("keeps headers of origin", () => { expect(a).toBe(1); });
"""

JAVA = """public class Vault {
  private int tries;
  public boolean open(int code) {
    try { throw new IllegalStateException("code is wrong"); }
    catch (IOException err) { log.warn("lost", err); } return true; }
  void spin() {}
  @Test void keepsHeadersOfOrigin() { assertEquals("headers were dropped", 1, 2); }
}
"""

RUST = """pub struct Vault { tries: i32 }
pub fn open(code: i32) -> Result<i32, String> {
    if code > 0 { return Err(format!("code {} is wrong", code)); }
    let _ = spin(); log::warn!("lost"); Ok(code) }
pub fn spin() {}
fn hidden() {}
#[test]
fn keeps_headers_of_origin() { assert_eq!(1, 2, "headers were dropped"); }
"""

RUBY = """class Vault
  def open(code)
    tries = 1
    raise ArgumentError, "code is wrong"
  rescue KeyError => err
    logger.warn("lost")
  end
end
it "keeps headers of origin" do
  expect(a).to eq(1)
  assert_equal 1, 2, "headers were dropped"
end
"""

CSHARP = """public class Vault {
  private int tries;
  public bool Open(int code) {
    try { throw new InvalidOperationException("code is wrong"); }
    catch (IOException err) { _logger.LogWarning("lost"); } return true; }
  private void Spin() {}
  [Fact] public void KeepsHeadersOfOrigin() { Assert.True(x, "headers were dropped"); }
}
"""

CPP = """class Vault {
 public:
  bool open(int code) {
    try { throw std::runtime_error("code is wrong"); }
    catch (const std::exception& err) { LOG(WARNING) << "lost"; } return true; }
};
TEST(VaultSuite, KeepsHeadersOfOrigin) { EXPECT_EQ(1, 2) << "headers were dropped"; }
TEST_CASE("keeps headers of origin") { REQUIRE(a == b); }
"""


def packs():
    return PackDirectory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "jev_gate", "packs")
    ).packs()


@pytest.mark.parametrize(
    "path, source, scope, names",
    [
        ("v.py", PYTHON, "type", ["Vault"]),
        ("v.py", PYTHON, "function", ["open", "test_keeps_headers_of_origin"]),
        ("v.py", PYTHON, "variable", ["code", "tries", "err"]),
        ("v.py", PYTHON, "throw", ['raise ValueError("code is wrong")']),
        ("v.py", PYTHON, "catch", ["except KeyError as err:"]),
        ("v.py", PYTHON, "log", ['logging.warning("lost %s", err)']),
        ("v.py", PYTHON, "test", ["test_keeps_headers_of_origin"]),
        ("v.js", JAVASCRIPT, "type", ["Vault"]),
        ("v.js", JAVASCRIPT, "function", ["open", "close"]),
        ("v.js", JAVASCRIPT, "test", ["keeps headers of origin"]),
        (
            "v.mjs",
            JAVASCRIPT,
            "catch",
            ['catch (err) { console.warn("lost", err); }', "promise.catch(() => {})"],
        ),
        ("v.ts", TYPESCRIPT, "type", ["Door", "Vault"]),
        ("v.ts", TYPESCRIPT, "function", ["open", "open", "close"]),
        ("v.tsx", TYPESCRIPT, "test", ["keeps headers of origin"]),
        ("V.java", JAVA, "type", ["Vault"]),
        ("V.java", JAVA, "function", ["open"]),
        ("V.java", JAVA, "test", ["keepsHeadersOfOrigin"]),
        ("V.java", JAVA, "log", ['log.warn("lost", err)']),
        ("v.rs", RUST, "type", ["Vault"]),
        ("v.rs", RUST, "function", ["open", "spin"]),
        ("v.rs", RUST, "test", ["keeps_headers_of_origin"]),
        ("v.rs", RUST, "catch", ["let _ = spin();"]),
        ("v.rs", RUST, "log", ['log::warn!("lost")']),
        ("v.rb", RUBY, "type", ["Vault"]),
        ("v.rb", RUBY, "test", ["keeps headers of origin"]),
        ("v.rb", RUBY, "throw", ['raise ArgumentError, "code is wrong"']),
        ("v.rb", RUBY, "catch", ["rescue KeyError => err"]),
        ("V.cs", CSHARP, "function", ["Open", "KeepsHeadersOfOrigin"]),
        ("V.cs", CSHARP, "test", ["KeepsHeadersOfOrigin"]),
        ("V.cs", CSHARP, "log", ['_logger.LogWarning("lost")']),
        ("v.cpp", CPP, "type", ["Vault"]),
        ("v.hpp", CPP, "test", ["KeepsHeadersOfOrigin", "keeps headers of origin"]),
        ("v.cc", CPP, "log", ['LOG(WARNING) << "lost";']),
    ],
)
def test_finds_candidates_of_each_language(
    path: str, source: str, scope: str, names: list[str]
):
    assert_that(
        [
            candidate.name()
            for candidate in SyntaxCandidates(FakeTree({path: source}), packs(), scope)
        ],
        contains_exactly(*names),
        f"The pack for '{path}' must find these '{scope}' candidates",
    )


@pytest.mark.parametrize(
    "path, source, fields, state",
    [
        ("w.py", PYTHON, ("phrase",), {"phrase": "it keeps headers of origin"}),
        (
            "w.py",
            PYTHON,
            ("message",),
            {"message": '"headers were dropped"\n"origin differs"'},
        ),
        ("w.js", JAVASCRIPT, ("message",), {"message": '"origin differs"'}),
        (
            "W.java",
            JAVA,
            ("phrase", "message"),
            {
                "phrase": "it keeps headers of origin",
                "message": '"headers were dropped"',
            },
        ),
        ("w.rs", RUST, ("message",), {"message": '"headers were dropped"'}),
        ("w.rb", RUBY, ("message",), {"message": '"headers were dropped"'}),
        ("W.cs", CSHARP, ("message",), {"message": '"headers were dropped"'}),
        ("w.cpp", CPP, ("message",), {"message": '"headers were dropped"'}),
    ],
)
def test_states_test_fields_of_each_language(
    path: str, source: str, fields: tuple[str, ...], state: dict[str, str]
):
    assert_that(
        next(iter(SyntaxCandidates(FakeTree({path: source}), packs(), "test")))
        .state(fields)
        .payload(),
        equal_to(state),
        f"The first test of '{path}' must state these fields",
    )


@pytest.mark.parametrize(
    "path, source, returns",
    [
        ("r.py", PYTHON, "bool"),
        ("r.ts", TYPESCRIPT, "boolean"),
        ("R.java", JAVA, "boolean"),
        ("r.rs", RUST, "Result<i32, String>"),
        ("R.cs", CSHARP, "bool"),
        ("r.cpp", CPP, "bool"),
    ],
)
def test_states_return_types_where_written(path: str, source: str, returns: str):
    assert_that(
        next(iter(SyntaxCandidates(FakeTree({path: source}), packs(), "function")))
        .state(("returns",))
        .payload(),
        equal_to({"returns": returns}),
        f"The first function of '{path}' must state its return type",
    )


@pytest.mark.parametrize("path, source", [("u.js", JAVASCRIPT), ("u.rb", RUBY)])
def test_leaves_return_types_unknown_where_unwritten(path: str, source: str):
    assert_that(
        next(iter(SyntaxCandidates(FakeTree({path: source}), packs(), "function")))
        .state(("returns",))
        .known(),
        equal_to(False),
        f"A function in '{path}' must have no known return type",
    )


def test_gives_rust_unit_for_a_missing_return_type():
    assert_that(
        [
            candidate.state(("returns",)).payload()["returns"]
            for candidate in SyntaxCandidates(
                FakeTree({"s.rs": RUST}), packs(), "function"
            )
        ],
        contains_exactly("Result<i32, String>", "()"),
        "A Rust function without a return type must return unit",
    )
