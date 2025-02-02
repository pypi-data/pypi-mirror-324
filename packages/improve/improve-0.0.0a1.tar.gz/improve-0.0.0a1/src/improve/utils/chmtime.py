#!/usr/bin/env -S python3 -OO

import argparse
import logging
import sys

from os import utime
from pathlib import Path
from datetime import datetime
from typing import cast


_logger = logging.getLogger()

LogLevel = int

DATE_FORMAT = 'YYYYMMDD-HHMMSS'


def _setup_logging(log_level: LogLevel) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    formatter = logging.Formatter(
        # '%(asctime)s %(levelname)-7s: %(message)s',
        '%(levelname)-7s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = cast(logging.Handler, logging.StreamHandler())

    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    root_logger.addHandler(handler)


def parse_mtime(mtime: str) -> datetime:
    try:
        return datetime.strptime(mtime, '%Y%m%d-%H%M%S')
    except ValueError:
        raise argparse.ArgumentTypeError('Date "{}" is\'nt in "{}" format.'.format(mtime, DATE_FORMAT))


def parse_filepath(path: str) -> Path:
    filepath = Path(path)
    if not filepath.exists():
        raise argparse.ArgumentTypeError('File "{}" does\'nt exists.'.format(filepath))
    return filepath


def _main() -> int:
    try:
        parser = argparse.ArgumentParser(
            description="""Set modification time of files.""",
            add_help=True,
        )
        verbosity_group = parser.add_mutually_exclusive_group(required=False)
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
            'mtime',
            action='store',
            type=parse_mtime,
            metavar='DATE',
            help='Date to set in "{}" format.'.format(DATE_FORMAT),
        )
        parser.add_argument(
            'files',
            action='append',
            type=parse_filepath,
            metavar='PATHS',
            help='Files to changes.',
        )

        args = parser.parse_args()

        log_level = logging.WARNING
        if args.debug:
            log_level = logging.DEBUG
        elif args.verbose:
            log_level = logging.INFO
        _setup_logging(log_level)
        del log_level

        mtime = args.mtime
        mtime_timestamp = mtime.timestamp()

        for filepath in args.files:
            _logger.info('Set date of "%s" to "%s".', filepath, mtime)
            utime(filepath, times=(mtime_timestamp, mtime_timestamp))
    except Exception as e:
        _logger.exception(str(e))
        return 1
    return 0


def main():
    sys.exit(_main())
