# Griffe Sphinx

[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://mkdocstrings.github.io/griffe-sphinx/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-708FCC.svg?style=flat)](https://gitpod.io/#https://github.com/mkdocstrings/griffe-sphinx)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#griffe-sphinx:gitter.im)

Parse Sphinx-comments above attributes as docstrings.

## Installation

This project is available to sponsors only, through my Insiders program.
See Insiders [explanation](https://mkdocstrings.github.io/griffe-sphinx/insiders/)
and [installation instructions](https://mkdocstrings.github.io/griffe-sphinx/insiders/installation/).

## Usage

Griffe Sphinx allows reading Sphinx comments above attribute assignments as docstrings.

```python
# your_module.py

#: Summary of your attribute.
#:
#: This is a longer description of your attribute.
#: You can use any markup in here (Markdown, AsciiDoc, rST, etc.).
#:
#: Be careful with indented blocks: they need 4 spaces plus the initial 1-space indent, so 5.
#:
#:     print("hello!")
your_attribute = "Hello Sphinx!"
```

This works for module attributes as well as class and instance attributes.

```python
class Hello:
    #: Summary of attribute.
    attr1 = "hello"

    def __init__(self):
        #: Summary of attribute.
        self.attr2 = "sphinx"
```

Trailing comments (appearing at the end of a line) are not supported.

You can now enable the extension when loading data with Griffe on the command-line, in Python code or with MkDocs.

**On the command-line:**

```bash
griffe dump your_package -e griffe_sphinx
```

**In Python code:**

```python
import griffe

data = griffe.load("your_package", extensions=griffe.load_extensions("griffe_sphinx"))
```

**With [MkDocs](https://www.mkdocs.org/):**

```yaml
plugins:
- mkdocstrings:
    handlers:
      python:
        options:
          extensions:
          - griffe_sphinx
```
