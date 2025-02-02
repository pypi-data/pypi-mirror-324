# coding: UTF-8

from __future__ import annotations

import logging
import sys
import os
import fcntl

from typing import Final


__all__: list[str] = [
    'StandardIOHandler',
    'FileLockHandler',
]

_log: Final[logging.Logger] = logging.getLogger(__name__)


class StandardIOHandler(logging.StreamHandler):

    def __init__(
            self,
            stdout=sys.stdout,
            stderr=sys.stderr,
            # level=logging.NOTSET,
            transition_level=logging.WARNING,
            debug_on_stderr=True,
    ):
        super(StandardIOHandler, self).__init__(stream=stderr)
        self.__stdout = stdout
        self.__stderr = stderr
        self.__transition_level = transition_level
        self.__debug_on_stderr = debug_on_stderr

    def emit(self, record):
        if record.levelno >= self.__transition_level or (
                record.levelno == logging.DEBUG and self.__debug_on_stderr
        ):
            self.stream = self.__stderr
        else:
            self.stream = self.__stdout
        super(StandardIOHandler, self).emit(record)


class FileLockHandler(logging.FileHandler):

    def __init__(
            self,
            filename,
            mode='a',
            encoding=None,
            delay=True,
            uid=None,
            gid=None,
    ):
        assert (uid is not None and gid is not None) or (uid is None and gid is None)
        self.__uid = uid
        self.__gid = gid
        super(FileLockHandler, self).__init__(
            filename,
            mode=mode,
            encoding=encoding,
            delay=delay,
        )

    def _open(self):
        stream = super(FileLockHandler, self)._open()
        assert (
            (self.__uid is not None and self.__gid is not None)
            or
            (self.__uid is None and self.__gid is None)
        )
        if self.__uid is not None and (os.getuid() != self.__uid or os.getgid() != self.__gid):
            os.chown(self.baseFilename, self.__uid, self.__gid)
        return stream

    def reopen(self):
        self.acquire()
        try:
            self.flush()
            if self.stream is not None and hasattr(self.stream, "close"):
                self.stream.close()
            self.stream = self._open()
        finally:
            self.release()

    def emit(self, record):
        try:
            if self.stream is None:
                self.stream = self._open()
            fcntl.lockf(self.stream.fileno(), fcntl.LOCK_EX)
            try:
                self.stream.seek(0, os.SEEK_END)
                super(FileLockHandler, self).emit(record)
            finally:
                if self.stream is not None:
                    fcntl.lockf(self.stream.fileno(), fcntl.LOCK_UN)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.handleError(record)
