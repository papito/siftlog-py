Sift Log - JSON logging adapter for Python (now in color)
===============

# Features
==========

* Tag log statements with arbitrary values for easier grouping and analysis

* Add keyword arguments that are converted to JSON values

* Variable substitution

* Specifies where log calls are made from

* Meant to be used with core Python logging (formatters, handlers, etc)

* Colorized logs on a console (POSIX only)

* `TRACE` log level built-in
 
# Examples
==========
### A simple log message
========================

```python

log.info('Hello')

```

`{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO", "loc": "test:log_test:20"}`

### Logging with tags
=====================

```python

log.debug('Creating new user', 'MONGO', 'STORAGE')

```

`{"msg": "Creating new user", "time": "12-12-14 10:12:09 EST", "tags": ["MONGO", "STORAGE"], "level": "DEBUG", "loc": "test:log_test:20"}`

### Appending more data
=======================

```python

log.debug('Some key', is_admin=True, username='papito')

```

`{"msg": "Some key", "is*admin": true, "username": "papito", "time": "12-12-14 10:12:04 EST", "level": "DEBUG", "loc": "test:log*test:20"}`

### String substitution
=======================

```python

log.debug('User "$username" admin? $is*admin', is*admin=False, username='fez')

```

`{"msg": "User \"fez\" admin? False",  "username": "fez", "is*admin": false, "time": "12-12-14 10:12:18 EST", "level": "DEBUG", "loc": "test:log*test:20"}`


# Setup
=======
### Logging to console
======================

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

In this fashion, you can direct the JSON logs to `any logging handler <https://docs.python.org/2/library/logging.handlers.html>`_

### Color
=========

For enhanced flamboyancy, attach the `ColorStreamHandler` to your logger. The output will not have color if the logs

are being output to a file, or on systems that are not POSIX (will not work on Windows for now).

```python

from siftlog import SiftLog, ColorStreamHandler

logger = logging.getLogger()

handler = ColorStreamHandler(sys.stdout)

logger.addHandler(handler)

log = SiftLog(logger)

```

#### Performance
================

While the above should play, it's highly recommended that the color handler is only 

attached conditionally for local development. Too many log statements could otherwise become

expensive in terms of CPU.


#### Different colors
=====================

You can change font background, text color, and boldness:

```python

from siftlog import ColorStreamHandler

handler = ColorStreamHandler(sys.stdout)

handler.set_color(

	logging.DEBUG, bg=handler.WHITE, fg=handler.BLUE, bold=True

)

```

#### Supported colors
=====================

 * ColorStreamHandler.BLACK

 * ColorStreamHandler.RED

 * ColorStreamHandler.GREEN

 * ColorStreamHandler.YELLOW

 * ColorStreamHandler.BLUE

 * ColorStreamHandler.MAGENTA

 * ColorStreamHandler.CYAN

 * ColorStreamHandler.WHITE

### Constants (re-occuring values)
==================================

You can define constants that will appear in every single log message. This is useful, for example, if you'd like to log process PID and hostname with every log message (recommended). This is done upon log adapter initialization:

```python

import os

from siftlog import SiftLog

log = SiftLog(logger, pid=os.getpid(), env='INTEGRATION')

```

`{"msg": "And here I am", "time": "12-12-14 11:12:24 EST", "pid": 37463, "env": "INTEGRATION", "level": "INFO"}`


### Custom time format
======================

```python

log = SiftLog(logger)

SiftLog.TIME_FORMAT = '%d-%m-%y %H:%m:%S %Z'

```

Define the format as accepted by `time.strftime() <https://docs.python.org/2/library/time.html#time.strftime>`_](https://docs.python.org/2/library/time.html#time.strftime)

### Custom location format
==========================

```python

log = SiftLog(logger)

SiftLog.LOCATION*FORMAT = '$module:$method:$line*no'

```

The format should be a string containing any of the following variables:

 * `$file`

 * `$line_no`

 * `$method`

 * `$module`

### Custom core key names
=========================

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

# Development flow
==================

`Poetry` is used to manage the dependencies.

Most things can be accessed via the Makefile, if you have Make installed.

	# use the right Python

	poetry use path/to/python/3.8\-ish

	# make sure correct Python is used

	make info

	# install dependencies

	make install

	# run tests

	make test

	# formatting, linting, and type checking

	make lint

