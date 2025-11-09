from __future__ import annotations

from typing import Any

import griffe

_logger = griffe.get_logger("griffe_sphinx")


class SphinxCommentsExtension(griffe.Extension):
    """Parse Sphinx-comments above attributes as docstrings."""

    def on_attribute_instance(
        self,
        *,
        attr: griffe.Attribute,
        agent: griffe.Visitor | griffe.Inspector,
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        """Parse Sphinx-comments above attributes as docstrings.

        Parameters:
            attr: The attribute being visited.
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
            lineno = attr.lineno - 2
            lines = []
            while lineno and (line := attr.lines_collection[attr.filepath][lineno].lstrip()).startswith("#:"):
                lines.append(line[3:])
                lineno -= 1
            if lines:
                attr.docstring = griffe.Docstring(
                    "\n".join(reversed(lines)),
                    lineno=lineno + 2,
                    endlineno=attr.lineno - 1,
                    parent=attr,
                    parser=agent.docstring_parser,
                    parser_options=agent.docstring_options,
                )
