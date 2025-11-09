# Griffe Sphinx

Parse Sphinx-comments above attributes as docstrings.

## Installation

```
pip install griffe-sphinx
```

## Usage

Griffe Sphinx allows reading Sphinx comments above attribute assignments as docstrings.

```
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

```
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

```
griffe dump your_package -e griffe_sphinx
```

**In Python code:**

```
import griffe

data = griffe.load("your_package", extensions=griffe.load_extensions("griffe_sphinx"))
```

**With [MkDocs](https://www.mkdocs.org/):**

```
plugins:
- mkdocstrings:
    handlers:
      python:
        options:
          extensions:
          - griffe_sphinx
```

## Sponsors
