Sift Log - JSON logging adapter for Python
===============

## Features
* Tag log statements with arbitrary values for easier grouping and analysis
* Add arbitrary keyword arguments that are converted to JSON values
* Variable sabstitution in log messages
* `TRACE` log level built-in
* Meant to be used with core Python logging (formatters, handlers, etc)
 
## Examples
#### A simple log message
```python
>>> log.info('Hello')
{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO"}`
```

#### Logging with tags
```python
>>> log.debug('Tags!', 'MONGO', 'DB')
{"msg": "Tags!", "time": "12-12-14 10:12:09 EST", "tags": ["tag.MONGO", "tag.DB"], "level": "DEBUG"}
```

#### Adding JSON keys
```python
>>> log.debug('Some key', is_admin = True, username='papito')
```
    {"msg": "Some key", "is_admin": true, "username": "papito", "time": "12-12-14 10:12:04 EST", "level": "DEBUG"}

#### String substitution
```python
>>> log.debug('User "$username" admin? $is_admin', is_admin = False, username='fez')
{"msg": "User \"fez\" admin? False",  "username": "fez", "is_admin": false, "time": "12-12-14 10:12:18 EST", "level": "DEBUG"}
```

## Setup
#### Logging to console
```python
import sys
import logging
from siftlog import SiftLog

logger = logging.getLogger()
logger.setLevel(logging.TRACE)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

log = SiftLog(logger)
```

## DOCS TODO
#### Custom time format

#### Custom core key names

#### Tag prefix

#### Custom JSON serialization

#### Constants


