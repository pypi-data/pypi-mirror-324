Python library improvements.

# Commands

## `waituntil`

Like bash function `sleep` but wait until a date is reached.  
If the date is already reached (exceeded), do not wait (exit immediately).

```commandline
$ waituntil '1970-01-01 01:00:00'; date
jeu. 01 janv. 1970 01:00:00 CET
$ waituntil '01:00'; date
jeu. 01 janv. 1970 01:00:00 CET
```

## `chmtime`

Set modification time of files.

```commandline
$ touch a_file
$ chmtime '19700101-010000' a_file
$ stat a_file |grep 'Modify:'
Modify: 1970-01-01 01:00:00.000000000 +0000
```

# functools helpers - `improve.functools`

## `improve.functools.wraps_keep_signature`

Like `functools.wraps` but keep the wrapped function signature.

## `improve.functools.retry`

Allows to redo treatments (a function) as long as it fails (with an exception),
and according to several criteria (delays before retry, with a backoff, etc.).

- `f`: treatments (`Callable[[], Any]`)
- `exceptions`: exceptions for which to retry
- `tries`: the number of attempts 
- `delay`: waiting time between attempts
- `max_delay`: maximum delay between attempts (limit if jitter and backoff increase too much)
- `backoff`: growth factor
- `jitter`: a fixed number, or random if a range tuple (min, max)
- `exception_callback`: a function which return bool, if true, continue to retry, else stop. Args: exception, waiting_delay, number_tries

A simple example:
```python
with retry(
        (
                lambda:
                    urlopen(
                        Request(
                            url,
                        ),
                        timeout=120,
                    )
        ),
        exceptions=(
                HTTPError,
                URLError,
                TimeoutError,
                IncompleteRead,
                RemoteDisconnected,
        ),
        tries=5,
        delay=2.5,
        max_delay=30.0,
        backoff=1.5,
        jitter=(0.1, 2.5),
) as response:
    ...
```

A minimalist example:
```python
# Try again to "compute" (to infinity) while there is an exception.
result = retry(compute)

with retry(
        (
                lambda: urlopen(Request(url))
        ),
        exceptions=(
                HTTPError,
                URLError,
                TimeoutError,
                IncompleteRead,
                RemoteDisconnected,
        ),
) as response:
    ...
```

A more complete example:

```python
_logger = logging.getLogger(...)

def retry_callback(e, waiting_delay, next_tries):
    if isinstance(e, HTTPError):
        if e.code in {
            404,
        }:
            return False
        _logger.warning(
            'Failed to fetch "%s" with error code "%s", retrying in %.01fs (%s tries)…',
            url,
            e.code,
            waiting_delay,
            next_tries,
        )
    elif isinstance(e, URLError):
        _logger.warning(
            'Failed to fetch "%s" with error reason "%s", retrying in %.01fs seconds (%s tries)…',
            url,
            e.reason,
            waiting_delay,
            next_tries,
        )
    elif isinstance(e, TimeoutError):
        _logger.warning(
            'Failed to fetch "%s" with timeout, retrying in %.01fs seconds (%s tries)…',
            url,
            waiting_delay,
            next_tries,
        )
    elif isinstance(e, ConnectionError):
        _logger.warning(
            'Failed to fetch "%s" with error "%s", retrying in %.01fs seconds (%s tries)…',
            url,
            e.strerror,
            waiting_delay,
            next_tries,
        )
    elif isinstance(e, IncompleteRead):
        if _logger.isEnabledFor(logging.WARNING):
            if e.expected is not None:
                message = 'Failed to fetch "%(url)s" with incomplete read error (%(read)i bytes received, %(expected)i more expected), retrying in %(delay).01fs seconds (%(tries)s tries)…'
            else:
                message = 'Failed to fetch "%(url)s" with incomplete read error (%(read)i bytes received), retrying in %(delay).01fs seconds (%(tries)s tries)…'
            _logger.warning(
                message,
                {
                    'url': url,
                    'read': len(e.partial),
                    'expected': e.expected,
                    'delay': waiting_delay,
                    'tries': next_tries,
                },
            )
    elif isinstance(e, RemoteDisconnected):
        if _logger.isEnabledFor(logging.WARNING):
            _logger.warning(
                'Failed to fetch "%s" with error "%s", retrying in %.01fs seconds (%s tries)…',
                url,
                str(e),
                waiting_delay,
                next_tries,
            )
    else:
        # Unexpected exception, not normal !
        return False
    return True


with retry(
        (
                lambda:
                    urlopen(
                        Request(
                            url,
                        ),
                        timeout=120,
                    )
        ),
        exceptions=(
                HTTPError,
                URLError,
                TimeoutError,
                IncompleteRead,
                RemoteDisconnected,
        ),
        tries=5,
        delay=2.5,
        max_delay=30.0,
        backoff=1.5,
        jitter=(0.1, 2.5),
        exception_callback=retry_callback,
) as response:
    ...
```

# logging helpers - `improve.logging`

## `improve.logging.decorator.logged`

A class decorator that add "_log" instance attribute

```python
@logged
class AClass:
    def afunc(self):
        self._log('afunc is called!')
```


## `improve.logging.handler.StandardIOHandler`

Handler allowing to log on stdout, but on stderr for warnings and beyond.

## `improve.logging.handler.FileLockHandler`

Handler for logging into a file competitively (with `fcntl` lock).

## `improve.logging.formatters.MultilineFormatter`

Formatter to apply the format of the logger to each record line.
