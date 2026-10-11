import tree_sitter
import tree_sitter_language_pack


class Grammar:
    def __init__(self, name: str):
        self.name = name
        self.compiled: dict[str, tree_sitter.Query] = {}

    def tree(self, data: bytes) -> tree_sitter.Tree:
        return tree_sitter.Parser(self._language()).parse(data)

    def query(self, source: str) -> tree_sitter.Query:
        if source not in self.compiled:
            try:
                self.compiled[source] = tree_sitter.Query(self._language(), source)
            except tree_sitter.QueryError as e:
                raise Exception(
                    f"A query for the '{self.name}' grammar does not compile"
                ) from e
        return self.compiled[source]

    def _language(self) -> tree_sitter.Language:
        try:
            return tree_sitter_language_pack.get_language(self.name)
        except Exception as e:
            raise Exception(f"The '{self.name}' grammar is not available") from e
