# friendly_names

[![PyPI - Version](https://img.shields.io/pypi/v/friendly-names.svg)](https://pypi.org/project/friendly-names)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/friendly-names.svg)](https://pypi.org/project/friendly-names)

A super simple random friendly name generator that creates readable, hyphenated names like "red-loop-bounty".

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Release Process](#release-process)
- [License](#license)

## Installation

```console
pip install friendly_names
```

## Usage

```python
import friendly_names

# Generate a friendly name like "red-loop-bounty"
name = friendly_names.generate()

# Customize number of words
name = friendly_names.generate(words=4)  # e.g., "happy-blue-running-fox"

# Use different separator
name = friendly_names.generate(separator="_")  # e.g., "green_swift_river"
```

## Development

To set up the development environment:

```console
pip install hatch
```

Common development tasks:

```console
# Run tests
hatch run test:test

# Run tests with coverage
hatch run test:coverage

# Run type checking
hatch run types:check

# Check code style
hatch run lint:style

# Format code
hatch run lint:fmt
```

The project uses:
- [Hatch](https://hatch.pypa.io/) for development environment and build management
- [pytest](https://docs.pytest.org/) for testing
- [mypy](https://mypy.readthedocs.io/) for type checking
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [Black](https://black.readthedocs.io/) style rules (via Ruff)

## Release Process

To release a new version:

1. Update version in `src/friendly_names/__about__.py`
2. Commit the change:
   ```console
   git add src/friendly_names/__about__.py
   git commit -m "Bump version to x.y.z"
   ```
3. Tag the release:
   ```console
   git tag -a vx.y.z -m "Release version x.y.z"
   ```
4. Push changes and tag:
   ```console
   git push origin master
   git push origin vx.y.z
   ```

The GitHub Actions workflow will automatically build and publish to PyPI when the tag is pushed.

## License

`friendly_names` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
