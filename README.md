Sift Log - JSON logging adapter for Python (now in color)
===============

![](https://raw.githubusercontent.com/papito/siftlog-py/master/assets/screen.png)

# Features
* Tag log statements with arbitrary values for easier grouping and analysis
* Add keyword arguments that are converted to JSON values
* Variable substitution
* Specifies where log calls are made from
* Colorized logs on a console (POSIX only)
* `TRACE` log level built-in
 
## Examples
### Setup (with no bells and whistles yet)

```python
import logging
from siftlog import SiftLog

core_logger = logging.getLogger()

logger = SiftLog(
    core_logger
)

logger.info('Hello')
```

`{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO"}`

### Logging with tags
```python
log.debug('Creating new user', 'MONGO', 'STORAGE')
```
`{"msg": "Creating new user",  "tags": ["MONGO", "STORAGE"], "level": "DEBUG",}`

### Appending more data
```python
log.debug('Some key', is_admin=True, username='papito')
```
`{"msg": "Some key", "is_admin": true, "username": "papito", "level": "DEBUG"}`

### String substitution
```python
log.debug('User "$username" admin? $is_admin', is_admin=False, username='fez')
```
`{"msg": "User \"fez\" admin? False",  "username": "fez", "is_admin": false, "level": "DEBUG"}`

Note that this is more performant than regular logging. String interpolation is *expensive*, possibly causing significant drag in a system with lots of log statements. With defferred string substituion, a log statement will never get expanded if it's not being logged at a given level in the first place.

### Constants (re-occurring values)
Logging is more noise than useful if you do not know the context of a log message. Which container is it running on? What environment is it in? Constants can be set up once, and they will stick throughout the lifecycle of a logger:


```python
import os
from siftlog import SiftLog

log = SiftLog(logger, pid=os.getpid(), env='INTEGRATION')
```

`{"msg": "Extremely hardcore", "pid": 37463, "env": "INTEGRATION", "level": "INFO"}`

### Dynamic logging context - callbacks
Often you need to add dynamic contextual data to log statements as opposed to one-time constants. SiftLog can except methods that will provide dynamic information depending on the context.

Logging request IDs or user IDs are very common use cases, so to log a thread-local property with Flask, for example,
we can do the following:

```python
import flask

def get_user_id():
    if flask.has_request_context():
        return flask.g.user_id

user_aware_logger = SiftLog(u_id=get_user_id)
```

`{"msg": "Logged in", u_id="200713391", "level": "INFO"}`

## Setup
### Logging to console
```python
import sys
import logging
from siftlog import SiftLog

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

log = SiftLog(logger)
```
In this fashion, you can direct the JSON logs to [any logging handler](https://docs.python.org/2/library/logging.handlers.html).

### Color
For enhanced flamboyancy, attach the `ColorStreamHandler` to your logger. The output will not have color if the logs
are being output to a file, or on systems that are not POSIX (will not work on Windows for now).

```python
from siftlog import SiftLog, ColorStreamHandler

logger = logging.getLogger()
handler = ColorStreamHandler(sys.stdout)
logger.addHandler(handler)

log = SiftLog(logger)
```

For development, you can opt in to use `ColorPlainTextStreamHandler`, for logs that are easier to parse visually.

#### Performance

While the above should play, it's highly recommended that the color handler is only 
attached conditionally for local development.


#### Different colors
You can change font background, text color, and boldness:

```python
from siftlog import ColorStreamHandler

handler = ColorStreamHandler(sys.stdout)
handler.set_color(
    logging.DEBUG, bg=handler.WHITE, fg=handler.BLUE, bold=True
)
```

#### Supported colors
 * ColorStreamHandler.BLACK
 * ColorStreamHandler.RED
 * ColorStreamHandler.GREEN
 * ColorStreamHandler.YELLOW
 * ColorStreamHandler.BLUE
 * ColorStreamHandler.MAGENTA
 * ColorStreamHandler.CYAN
 * ColorStreamHandler.WHITE

### Custom time format
```python
log = SiftLog(logger)
SiftLog.TIME_FORMAT = '%Y/%m/%d %H:%M:%S.%f'
```
Define the format as accepted by [strftime()](https://strftime.org/)

### Custom location format
```python
log = SiftLog(logger)
SiftLog.LOCATION_FORMAT = '$module:$method:$line_no'
```
The format should be a string containing any of the following variables:

 * `$file`
 * `$line_no`
 * `$method`
 * `$module`

### Custom core key names
Core keys, such as `msg` and `level` can be overridden, if they clash with common keys you might be using.

The following can be redefined:

 * SiftLog.MESSAGE (default `msg`)
 * SiftLog.LEVEL (default `level`)
 * SiftLog.LOCATION (default `loc`)
 * SiftLog.TAGS (default `tags`)
 * SiftLog.TIME (default `time`)

As in:

```python
log = SiftLog(logger)
SiftLog.log.MESSAGE = "MESSAGE"
```

## Development flow

`Poetry` is used to manage the dependencies.

Most things can be accessed via the Makefile, if you have Make installed.
Without Make, just inspect the Makefile for the available commands.

    # use the right Python
    poetry use path/to/python/3.8-ish
    
    # make sure correct Python is used
    make info
    
    # install dependencies
    make install
    
    # run tests
    make test
    
    # run visual tests (same as tests but with output)
	make visual
    
    # formatting, linting, and type checking
    make lint

### Running a single test

In the standard Nose tests way:

    poetry run nosetests siftlog/tests/test_log.py:TestLogger.test_tags
