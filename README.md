Sift Log - JSON logging adapter for Python
===============

## Features
* Tag log statements with arbitrary values for easier grouping and analysis
* Add keyword arguments that are converted to JSON values
* Variable substitution
* Specifies where log calls are made from
* Meant to be used with core Python logging (formatters, handlers, etc)
* `TRACE` log level built-in
 
## Examples
#### A simple log message
```python
log.info('Hello')
```
`{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO", "loc": "test:log_test:20"}`

#### Logging with tags
```python
log.debug('Creating new user', 'MONGO', 'STORAGE')
```
`{"msg": "Creating new user", "time": "12-12-14 10:12:09 EST", "tags": ["MONGO", "STORAGE"], "level": "DEBUG", "loc": "test:log_test:20"}`

#### Adding JSON keys
```python
log.debug('Some key', is_admin=True, username='papito')
```
`{"msg": "Some key", "is_admin": true, "username": "papito", "time": "12-12-14 10:12:04 EST", "level": "DEBUG", "loc": "test:log_test:20"}`

#### String substitution
```python
log.debug('User "$username" admin? $is_admin', is_admin=False, username='fez')
```
`{"msg": "User \"fez\" admin? False",  "username": "fez", "is_admin": false, "time": "12-12-14 10:12:18 EST", "level": "DEBUG", "loc": "test:log_test:20"}`


## Setup
#### Logging to console
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

In this fashion, you can direct the JSON logs to [any logging handler](https://docs.python.org/2/library/logging.handlers.html)

#### Constants (re-occuring values)
You can define constants that will appear in every single log message. This is useful, for example, if you'd like to log process PID and hostname with every log message (recommended). This is done upon log adapter initialization:

```python
import os
from siftlog import SyftLog
log = SiftLog(logger, pid=os.getpid(), env='INTEGRATION')
```
`{"msg": "And here I am", "time": "12-12-14 11:12:24 EST", "pid": 37463, "env": "INTEGRATION", "level": "INFO"}`


#### Custom time format
Define `SiftLog.TIME_FORMAT`, accepted by [time.strftime()](https://docs.python.org/2/library/time.html#time.strftime)

#### Custom core key names
Core keys, such as `msg` and `level` can be overridden, if they clash with common keys you might be using.

The following can be redefined:

 * __SiftLog.MESSAGE__ (default `msg`)
 * __SiftLog.LEVEL__ (default `level`)
 * __SiftLog.LOCATION__ (default `loc`)
 * __SiftLog.TAGS__ (default `tags`)
 * __SiftLog.TIME__ (default `time`)
