# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2024, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Tests for the extension module."""

from __future__ import annotations

from textwrap import dedent

import griffe

from griffe_sphinx import SphinxCommentsExtension


def test_extension() -> None:
    """Fetch comments from source."""
    with griffe.temporary_visited_module(
        """\
        #: Summary for `a`.
        #:
        #: Description for `a`.
        a = 0

        class C:
            #: Summary for `b`.
            #:
            #: Description for `b`.
            #:
            #: Warning:
            #:     Indentation must work.
            b = 1

            def __init__(self):
                #: Summary for `i`.
                #:
                #: Description for `i`.
                self.i = 2
                self.j = C.b  #: Summary for `j` (inline).
                self.k: str  #: Summary for `k` (inline).
                self.l = "#: not a doc comment"  # still not a `#:` doc comment

        """,
        extensions=griffe.load_extensions(SphinxCommentsExtension),
    ) as module:
        assert module["a"].docstring.value == "Summary for `a`.\n\nDescription for `a`."
        assert module["a"].docstring.lineno == 1
        assert module["a"].docstring.endlineno == 3
        assert (
            module["C.b"].docstring.value
            == dedent("""\
            Summary for `b`.

            Description for `b`.

            Warning:
                Indentation must work.
        """)[:-1]
        )
        assert module["C.i"].docstring.value == "Summary for `i`.\n\nDescription for `i`."
        assert module["C.j"].docstring.value == "Summary for `j` (inline)."
        assert module["C.k"].docstring.value == "Summary for `k` (inline)."
        assert not module["C.l"].has_docstring
