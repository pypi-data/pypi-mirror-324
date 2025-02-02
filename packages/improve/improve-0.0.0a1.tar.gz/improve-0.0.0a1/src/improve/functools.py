# coding: UTF-8

from __future__ import annotations

import logging
import random
import time

from functools import (
    WRAPPER_ASSIGNMENTS,
    partial,
    wraps,
)
from typing import (
    Final,
    Literal,
    cast,
    get_args,
)


__all__: list[str] = [
]

_log: Final[logging.Logger] = logging.getLogger(__name__)


WrapperAssignedType: TypeAlias = Literal[  # type: ignore[valid-type]
    cast(
        tuple[
            str,
            ...,
        ],
        WRAPPER_ASSIGNMENTS,
    )
]
WRAPPER_ASSIGNMENTS_WITHOUT_ANNOTATIONS: tuple[WrapperAssignedType, ...] = tuple(
    set(
        get_args(
            WrapperAssignedType,
        ),
    ) - {
        '__annotations__',
    },
)


wraps_keep_signature = partial(
    wraps,
    assigned=WRAPPER_ASSIGNMENTS_WITHOUT_ANNOTATIONS,
)


def retry(
    f,
    exceptions=Exception,
    tries=float('inf'),
    delay=0.0,
    max_delay=None,
    backoff=1.0,
    jitter=0.0,  # fixed number, or random if a range tuple (min, max)
    exception_callback=None,  # return bool, if true, continue to retry, else stop. Args: exception, waiting_delay, number_tries
):
    assert tries >= 1
    current_tries = 1
    assert current_tries <= tries
    current_delay = delay
    while True:
        try:
            return f()
        except exceptions as e:
            assert current_tries <= tries
            if current_tries == tries:
                raise

            current_tries += 1
            if exception_callback is not None:
                continue_ = exception_callback(e, current_delay, current_tries)
                assert isinstance(continue_, bool)
                if continue_ is False:
                    raise

            time.sleep(current_delay)
            # Next delay
            current_delay *= backoff

            if isinstance(jitter, tuple):
                current_delay += random.uniform(*jitter)
            else:
                current_delay += jitter

            if max_delay is not None:
                current_delay = min(current_delay, max_delay)
