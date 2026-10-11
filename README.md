# Jev Gate

A GitHub Action that fails a pipeline when code breaks a quality rule that
only a reader could check. Rules are yes/no questions in a YAML file; code
picks what each question applies to, [Jev](https://docs.typesafe.ai) answers
with a probability, and code compares it with a threshold.

## Usage

```yaml
- uses: actions/checkout@v7
  with:
    fetch-depth: 0
    ref: ${{ github.event.pull_request.head.sha }}
- uses: your-org/jev-gate@v1
  with:
    config: .github/jev-gates.yml
    mode: diff
    base: ${{ github.event.pull_request.base.sha }}
  env:
    TYPESAFE_API_KEY: ${{ secrets.TYPESAFE_API_KEY }}
```

`fetch-depth: 0` is required in `diff` mode: the base commit must be in the
history. Checking out the head commit keeps the merge commit of a pull
request out of the `commit` scope.

| Exit code | Meaning |
| --- | --- |
| 0 | No gate fired |
| 1 | At least one gate fired |
| 2 | The tool could not finish |

## Gates file

See [examples/jev-gates.yml](examples/jev-gates.yml). Top-level keys:

| Key | Purpose |
| --- | --- |
| `model` | Pinned Jev version, such as `jev-1.13.0`. Aliases are refused. |
| `oversize` | `fail` (default) or `skip` |
| `paths` | `include` and `exclude` globs; `**` crosses directories |
| `scopes` | Custom syntax scopes (see below) |
| `gates` | The gates |

Gate keys: `id`, `rule`, `scope`, `allow`, `state`, `ask`, `fail_above`,
`modes`, `oversize`. A gate fires when the probability is strictly above
`fail_above`. `allow` lists candidate names the gate never judges: the
identifier for `type`, `function` and `variable`, the raw test name for
`test`, the path for `file` and `hunk`, and the subject for `commit`.
`where` filters are not supported yet.

Gates of one candidate that send the same `state` fields share one request.

## Custom scopes

A custom scope gives a tree-sitter query per language pack. Captures name
the fields; `@candidate` marks the node, and captures starting with `_`
are ignored.

```yaml
scopes:
  bdd_step:
    fields: [phrase, source]
    packs:
      python:
        match: |
          ((decorated_definition
             (decorator) @_d
             definition: (function_definition name: (identifier) @phrase)) @candidate @source
           (#match? @_d "^@(given|when|then)"))
```

## Development

```sh
uv venv .venv && uv pip install --python .venv -e ".[dev]"
make unit      # fast tests with coverage
make e2e       # deep tests
make black flake8 ruff
```
