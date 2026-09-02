"""Griffe Sphinx package.

Parse Sphinx-comments about attributes as docstrings.
"""

from __future__ import annotations

from griffe_sphinx._internal.extension import SphinxCommentsExtension

__all__: list[str] = ["SphinxCommentsExtension"]
