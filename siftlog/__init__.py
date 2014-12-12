import os
import logging
import json
import inspect
import time
from string import Template

logging.TRACE = 5
logging.addLevelName(logging.TRACE, 'TRACE')

class SiftLog(logging.LoggerAdapter):
    MESSAGE     = 'msg'
    LEVEL       = 'level'
    LOCATION    = 'loc'
    TAGS        = 'tags'
    TIME        = 'time'
    TAG_PREFIX  = 'tag.'
    TIME_FORMAT = '%d-%m-%y %H:%m:%S %Z'

    def __init__(self, logger, **kwargs):
        super(SiftLog, self).__init__(logger, {})
        self.constants = kwargs

    def _get_log_stmt(self, level, msg, *tags, **kwargs):
        msg = msg or ''

        kwargs[self.LEVEL] = logging.getLevelName(level)

        # append the optional constants defined on initialization
        kwargs.update(self.constants)

        # add message to the payload, substitute with the passed data
        kwargs[self.MESSAGE] = Template(msg).safe_substitute(kwargs)

        # caller info
        frm = inspect.stack()[3]
        mod = inspect.getmodule(frm[0])
        if mod:
            line_no = frm[2]
            method  = frm[3]
            module  = mod.__name__
            loc = kwargs[self.LOCATION] = '%s:%s:%s' % (module, method, line_no)

        kwargs[self.TIME] = self.get_timestamp()

        if tags and self.TAG_PREFIX:
            kwargs[self.TAGS] = [self.TAG_PREFIX + tag for tag in tags]

        try:
            payload = self.to_json(kwargs)
        except (Exception) as ex:
            msg = 'LOGGER EXCEPTION "{0}" in  {1}'.format(str(ex), loc)
            return json.dumps({
                'msg': msg,
                'level': logging.getLevelName(logging.ERROR)
            })

        return payload

    def to_json(self, data):
        return json.dumps(data)

    def get_timestamp(self):
        return time.strftime(self.TIME_FORMAT)

    def trace(self, msg, *args, **kwargs):
        if not self.logger.isEnabledFor(logging.TRACE):
            return 

        self.log(logging.TRACE, msg,  *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if not self.logger.isEnabledFor(logging.DEBUG):
            return 

        self.log(logging.DEBUG, msg,  *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if not self.logger.isEnabledFor(logging.INFO):
            return 

        self.log(logging.INFO, msg,  *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if not self.logger.isEnabledFor(logging.WARNING):
            return 

        self.log(logging.WARNING, msg,  *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if not self.logger.isEnabledFor(logging.ERROR):
            return 

        self.log(logging.ERROR, msg,  *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if not self.logger.isEnabledFor(logging.CRITICAL):
            return 

        self.log(logging.CRITICAL, msg,  *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        payload = self._get_log_stmt(level, msg, *args, **kwargs)
        self.logger.log(level, payload)
