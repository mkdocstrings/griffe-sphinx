"""Tests for the extension module."""

from __future__ import annotations

import griffe

from griffe_sphinx import SphinxCommentsExtension


def test_extension() -> None:
    """Fetch comments from source."""
    with griffe.temporary_visited_module(
        """
        #: Summary for `a`.
        #:
        #: Description for `a`.
        a = 0

        class C:
            #: Summary for `b`.
            #:
            #: Description for `b`.
            b = 1

            def __init__(self):
                #: Summary for `i`.
                #:
                #: Description for `i`.
                self.i = 2

        """,
        extensions=griffe.load_extensions(SphinxCommentsExtension),
    ) as module:
        assert module["a"].docstring.value == "Summary for `a`.\n\nDescription for `a`."
        assert module["C.b"].docstring.value == "Summary for `b`.\n\nDescription for `b`."
        assert module["C.i"].docstring.value == "Summary for `i`.\n\nDescription for `i`."
