# godolint-coatl

[![GitHub Release](https://img.shields.io/github/v/release/coatl-dev/godolint-coatl)](https://github.com/coatl-dev/godolint-coatl/releases/latest)
[![Downloads](https://static.pepy.tech/badge/godolint-coatl)](https://pepy.tech/project/godolint-coatl)

A python wrapper to provide a pip-installable [godolint] binary. Inspired by
[shellcheck-py].

Internally this package provides a convenient way to download the pre-built
godolint binary for your particular platform.

## Installation

```bash
pip install godolint-coatl
```

## Usage

After installation, the `godolint` binary should be available in your
environment (or `godolint.exe` on Windows).

### As a pre-commit hook

See [pre-commit] for instructions

Sample `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/coatl-dev/godolint-coatl
    rev: 1.0.3
    hooks:
      - id: godolint
```

[godolint]: https://github.com/zabio3/godolint
[pre-commit]: https://pre-commit.com
[shellcheck-py]: https://github.com/shellcheck-py/shellcheck-py
