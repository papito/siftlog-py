Sift Log - JSON logging adapter for Python
===============

## Features
* Tag log statements with arbitrary values for easier grouping and analysis
* Add arbitrary keyword arguments that are converted to JSON values
* Variable substitution in log messages
* `TRACE` log level built-in
* Meant to be used with core Python logging (formatters, handlers, etc)
 
## Examples
#### A simple log message
```python
log.info('Hello')
```
`{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO"}`

#### Logging with tags
```python
log.debug('Tags!', 'MONGO', 'DB')
```
`{"msg": "Tags!", "time": "12-12-14 10:12:09 EST", "tags": ["tag.MONGO", "tag.DB"], "level": "DEBUG"}`

#### Adding JSON keys
```python
log.debug('Some key', is_admin = True, username = 'papito')
```
`{"msg": "Some key", "is_admin": true, "username": "papito", "time": "12-12-14 10:12:04 EST", "level": "DEBUG"}`

#### String substitution
```python
log.debug('User "$username" admin? $is_admin', is_admin = False, username = 'fez')
```
`{"msg": "User \"fez\" admin? False",  "username": "fez", "is_admin": false, "time": "12-12-14 10:12:18 EST", "level": "DEBUG"}`


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

In this fashion, you can direct the JSON logs to [any core logging handler](https://docs.python.org/2/library/logging.handlers.html)

#### Constants (re-occuring values)
You can define constants that will appear in every single log message. This is useful, for example, if you'd like to log process PID and hostname with every log message (recommended). This is done upon log adapter initialization:

```python
import os
from siftlog import SyftLog
log = SiftLog(logger, pid = os.getpid(), env='INTEGRATION')
```
`{"msg": "And here I am", "time": "12-12-14 11:12:24 EST", "pid": 37463, "env": "INTEGRATION", "level": "INFO"}`



#### Custom time format
Define `SiftLog.TIME_FORMAT`, accepted by [time.strftime()](https://docs.python.org/2/library/time.html#time.strftime)

#### Custom core key names
Key names, such as `msg` and `level` can be overridden, if they clash with common keys you might be using.

The following can be redefined:

 * __SiftLog.MESSAGE__ (default `msg`)
 * __SiftLog.LEVEL__ (default `level`)
 * __SiftLog.LOCATION__ (default `loc`)
 * __SiftLog.TAGS__ (default `tags`)
 * __SiftLog.TIME__ (default `time`)

#### Tag prefix
Arbitrary tags by default are prefixed with `tag.`, for easier searching. The prefix can be changed, or removed, by redefining `SiftLog.TAG_PREFIX`

```python
SiftLog.to_json = def to_json(self, data): = 
```



