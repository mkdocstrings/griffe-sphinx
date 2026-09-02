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

from __future__ import annotations

import ast
from textwrap import dedent
from typing import Any

import griffe

_logger = griffe.get_logger("griffe_sphinx")


class SphinxCommentsExtension(griffe.Extension):
    """Parse Sphinx-comments about attributes as docstrings."""

    def on_attribute_instance(
        self,
        *,
        node: ast.AST | griffe.ObjectNode,
        attr: griffe.Attribute,
        agent: griffe.Visitor | griffe.Inspector,
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        """Parse Sphinx-comments about attributes as docstrings.

        Parameters:
            node: The attribute node being visited.
            attr: The attribute being built.
            agent: The visitor or inspector visiting the attribute.
            **kwargs: Additional keyword arguments.
        """
        if attr.docstring is None:
            if attr.lineno is None or attr.endlineno is None:
                _logger.debug(f"Skipping Sphinx-comments parsing for {attr.path}: lineno or endlineno is None")
                return
            if isinstance(attr.filepath, list):
                # This should never happen (an attribute cannot be defined in a directory/native-namespace package),
                # but for good measure we handle the case.
                return
            # Look for doc comments in preceding lines first.
            file_lines = attr.lines_collection[attr.filepath]
            line_index = attr.lineno - 2  # -1 to go back one line, -1 to convert to a 0-based index.
            lines = []
            while line_index >= 0 and (line := file_lines[line_index].lstrip()).startswith("#:"):
                lines.append(line[2:])
                line_index -= 1
            if lines:
                attr.docstring = griffe.Docstring(
                    dedent("\n".join(reversed(lines))),
                    lineno=line_index + 2,
                    endlineno=attr.lineno - 1,
                    parent=attr,
                    parser=agent.docstring_parser,
                    parser_options=agent.docstring_options,
                )
                return
            # Otherwise look for inline trailing comments.
            if attr.endlineno != attr.lineno:  # not supported for multi-line assignments
                return
            if not isinstance(node, ast.AST):
                # Parse the source, as ObjectNodes have no source-related data (column offsets).
                try:
                    node = ast.parse(attr.source).body[0]
                except (SyntaxError, IndexError):
                    _logger.debug(f"Skipping Sphinx-comments parsing for {attr.path}: ast parsing failed")
                    return
            try:
                has_col_offsets = node.col_offset is not None and node.end_col_offset is not None
            except AttributeError:
                # This shouldn't happen, as node would be an instance of ast.Assign or ast.AnnAssign.
                has_col_offsets = False
            if not has_col_offsets:
                _logger.debug(f"Skipping Sphinx-comments parsing for {attr.path}: node missing col offset")
                return
            node_end_in_source = node.end_col_offset - node.col_offset
            try:
                comment = attr.source[node_end_in_source:].split("#", maxsplit=1)[1]
            except IndexError:
                return
            if comment.startswith(":"):
                attr.docstring = griffe.Docstring(
                    comment[1:].lstrip(),
                    lineno=attr.lineno,
                    endlineno=attr.lineno,
                    parent=attr,
                    parser=agent.docstring_parser,
                    parser_options=agent.docstring_options,
                )
