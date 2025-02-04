# steev

`steev` is a CLI agent to automate your ML experiments.

## Installation

Now we only support build from source. To build from source, you need to have [poetry](https://python-poetry.org/) installed.

### Install poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Build from source

```bash
poetry install
```

## Contribution

To contribute to `steev`, you need to install dependencies and run pre-commit hooks. We use [poetry](https://python-poetry.org/) to manage dependencies and [pre-commit](https://pre-commit.com/) to run pre-commit hooks.

### Install dependencies

Use `poetry` to install dependencies and `pre-commit` to run pre-commit hooks.

```bash
poetry install --with dev
poetry run pre-commit
```

### Development dependencies

- [poetry](https://python-poetry.org/): Dependency management
- [pre-commit](https://pre-commit.com/): Pre-commit hooks
- [ruff](https://github.com/astral-sh/ruff): Linter
- [black](https://github.com/psf/black): Formatter
- [mypy](https://github.com/python/mypy): Static type checker
