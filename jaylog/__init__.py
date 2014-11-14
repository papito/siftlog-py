import os
import logging
import json
import inspect
import datetime
from string import Template

class LogAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        super(LogAdapter, self).__init__(logger, {})

    def _get_log_stmt(self, level, msg, *tags, **kwargs):
        frm = inspect.stack()[3]
        mod = inspect.getmodule(frm[0])

        # add message to the payload, substite with the passed data
        kwargs['msg'] = Template(msg).safe_substitute(kwargs)

        kwargs['level'] = logging.getLevelName(level)

        if mod:
            # caller info
            line_no = frm[2]
            method  = frm[3]
            module  = mod.__name__
            loc = kwargs['loc'] = '%s:%s:%s' % (module, method, line_no)

        kwargs['time'] = str(datetime.datetime.now()) 

        if tags:
            kwargs['tags'] = ['tag.' + tag for tag in tags]

        # delete keys we don't want (sometimes to save space and network traffic)
        if 'without' in kwargs:
            omit_keys = kwargs.get('without', [])
            for omit_key in omit_keys:
                if omit_key in kwargs:
                    del kwargs[omit_key]
            del kwargs['without']
            
        payload = ''

        try:
            payload = json.dumps(kwargs)

        except Exception, ex:
            msg = 'LOGGER EXCEPTION "{0}" in  {1}'.format(str(ex), loc)
            return json.dumps({
                'msg': msg,
                'level': logging.getLevelName(logging.ERROR)
            })

        return payload

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
