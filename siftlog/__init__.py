import os
import logging
import json
import inspect
import time
import itertools
from string import Template

logging.TRACE = 5
logging.addLevelName(logging.TRACE, 'TRACE')

class SiftLog(logging.LoggerAdapter):
    MESSAGE     = 'msg'
    LEVEL       = 'level'
    LOCATION    = 'loc'
    TAGS        = 'tags'
    TIME        = 'time'
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

        # caller location
        loc = self.get_caller_info()
        if loc:
            kwargs[self.LOCATION] = loc

        kwargs[self.TIME] = self.get_timestamp()

        if tags:
            kwargs[self.TAGS] = tags

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

    def get_caller_info(self):
        loc = self._get_caller_info()

        if not loc:
            return None

        module, method, line_no = loc
        return '%s:%s:%s' % (module, method, line_no)

    def _get_caller_info(self):
        # pull the frames from the current stack, reversed,
        # since it's easier to find the first siftlog frame
        frames = [
            (idx, frm, inspect.getmodule(frm[0])) 
            for idx, frm 
            in enumerate(reversed(inspect.stack()))
        ]

        # travel the stack from behind, looking for the first siftlog frame
        res = itertools.dropwhile(lambda (idx, f, m): m and m.__name__ != 'siftlog' , frames)
        # the first siftlog frame from back of the stack
        siftlog_frame = res.next()
        # its index
        siftlog_frame_idx = siftlog_frame[0]

        if siftlog_frame_idx == 0: # there is no caller module (console)
            return None

        # the frame before this one is what's calling the logger
        frm = frames[siftlog_frame_idx - 1][1]

        # now get the caller info
        mod = inspect.getmodule(frm[0])
        line_no = frm[2]
        method  = frm[3]
        module  = mod.__name__

        return module, method, line_no

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

    def warn(self, msg, *args, **kwargs):
        self.warning(msg, *args, **kwargs)

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
