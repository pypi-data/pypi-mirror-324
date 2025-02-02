# coding: UTF-8

from __future__ import annotations

import argparse
import logging
import re
import sys

from datetime import (
    datetime,
    date,
    timedelta,
)
from time import sleep
from typing import (
    Final,
    cast,
)


__all__: list[str] = [
]

_log: Final[logging.Logger] = logging.getLogger(__name__)

LogLevel = int


_READABLE_UNTIL_DATE_FORMAT = '[YYYY-MM-DD ]HH:MM[:SS]'
_re_until_date = re.compile(r'^(?:(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) )?(?P<hour>\d{2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?$')


def _until_date(until: str) -> datetime:
    groups = _re_until_date.search(until)
    if groups is None:
        raise ValueError('"{} isn\'t in excpected format {}."'.format(until, _READABLE_UNTIL_DATE_FORMAT))
    
    # date
    parsed_year = groups.group('year')
    if parsed_year is not None:
        year = int(parsed_year, 10)
        assert groups.group('month') is not None
        assert groups.group('day') is not None

        month = int(groups.group('month'), 10)
        day = int(groups.group('day'), 10)
    else:
        assert groups.group('month') is None
        assert groups.group('day') is None

        today = date.today()
        year = today.year
        month = today.month
        day = today.day 

    # time
    hour = int(groups.group('hour'), 10)
    minute = int(groups.group('minute'), 10)
    parsed_second = groups.group('second')
    if parsed_second is not None:
        second = int(parsed_second, 10)
    else:
        second = 0

    assert isinstance(year, int)
    assert isinstance(month, int)
    assert isinstance(day, int)
    assert isinstance(hour, int)
    assert isinstance(minute, int)
    assert isinstance(second, int)
    return datetime(year, month, day, hour, minute, second)


def _setup_logging(log_level: LogLevel) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)-7s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = cast(logging.Handler, logging.StreamHandler())

    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    root_logger.addHandler(handler)


def _main() -> int:
    try:
        parser = argparse.ArgumentParser(
            description="""Wait until date.""",
            add_help=True,
        )
        verbosity_group = parser.add_mutually_exclusive_group(required=False)
        verbosity_group.add_argument(
            '-q',
            '--quiet',
            action='store_true',
            default=False,
            help='Set verbosity level to ERROR.'
        )
        verbosity_group.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='Set verbosity level to INFO.'
        )
        verbosity_group.add_argument(
            '-d',
            '--debug',
            action='store_true',
            default=False,
            help='Set verbosity level to DEBUG.'
        )
        parser.add_argument(
            'date',
            action='store',
            type=_until_date,
            metavar='date',
            help='in format {}.'.format(_READABLE_UNTIL_DATE_FORMAT),
        )

        args = parser.parse_args()

        log_level = logging.WARNING
        if args.debug:
            log_level = logging.DEBUG
        elif args.verbose:
            log_level = logging.INFO
        elif args.quiet:
            log_level = logging.ERROR
        _setup_logging(log_level)
        del log_level

        until = args.date
        now = datetime.now()
        waiting = until - now
        if waiting <= timedelta(0):
            _log.warning('%s is already been reached, no waiting.', until)
            return 0
        waiting_seconds = waiting.total_seconds()
        _log.info(
            'Wait until %s is reached, that is %s (%0.3f seconds).',
            until,
            waiting,
            waiting_seconds,
        )

        try:
            sleep(waiting_seconds)
        except KeyboardInterrupt:
            if _log.isEnabledFor(logging.WARNING) is True:
                current_now = datetime.now()
                time_passed = current_now - now
                time_missing = until - current_now
                _log.warning(
                    'The wait was interrupted at %s, after %s (%0.3f seconds) of waiting and %s (%0.3f seconds) too early.',
                    current_now,
                    time_passed,
                    time_passed.total_seconds(),
                    time_missing,
                    time_missing.total_seconds(),
                )
            return 1
    except Exception as e:
        _log.exception(str(e))
        return 2
    return 0


def main():
    sys.exit(_main())
