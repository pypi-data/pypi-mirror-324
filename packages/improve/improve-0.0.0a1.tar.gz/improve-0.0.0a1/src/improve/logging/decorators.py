# coding: UTF-8

from __future__ import annotations

import logging

from typing import Final


__all__: list[str] = [
    'logged',
]

_log: Final[logging.Logger] = logging.getLogger(__name__)

def _get_instance_logger(self):
    try:
        return getattr(self, '__logger_instance')
    except AttributeError:
        logger = logging.getLogger(
            '{}.{}'.format(
                self.__module__,
                self.__class__.__name__,
            ),
        )
        setattr(self, '__logger_instance', logger)
        return logger


def logged(cls):
    """A class decorator that add "_log" instance attribute

    The "_log" attribute is a logging.Logger initialized with
    module and class names.
    """
    assert isinstance(cls, type)
    if not hasattr(cls, '_log'):
        setattr(cls, '_log', property(fget=_get_instance_logger))
    return cls
