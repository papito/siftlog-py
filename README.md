Sift Log - JSON logging adapter for Python
===============

## Features
* Tag log statements with arbitray values for easier grouping and analysis
* Add arbitrary keyword arguments that are converted to JSON values
* Variable sabstitution in log messages
* Has the `TRACE` log level built-in
* Meant to be used with core Python logging (formatters, handlers, etc)
 
## Examples

#### A simple log message

```python
>>> log.info('Hello')
{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO"}
```
