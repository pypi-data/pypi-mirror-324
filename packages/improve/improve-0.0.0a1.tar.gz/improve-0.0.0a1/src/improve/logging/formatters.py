# coding: UTF-8

from __future__ import annotations

import logging

from typing import Final


__all__: list[str] = [
    'MultilineFormatter',
]

_log: Final[logging.Logger] = logging.getLogger(__name__)


class MultilineFormatter(logging.Formatter):

    def _format_lines(self, text, record_dict, format_first_line=True):
        formatted_lines = []
        lines = text.split("\n")
        if not format_first_line:
            formatted_lines.append(lines.pop(0))
        for line in lines:
            record_dict['message'] = line
            formatted_lines.append(self._fmt % record_dict)
        return u"\n".join(formatted_lines)

    def format(self, record):
        """ Like logging.Formatter.format but apply format for all lines """
        return self._format_lines(
            super().format(record),
            record.__dict__,
            format_first_line=False,
        )
