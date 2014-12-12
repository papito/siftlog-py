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
{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO"}
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

