import os
import sys
import logging
import json
import collections
import inspect
import traceback
import datetime
from string import Template

"""
import jaylog, sys, logging; logger = logging.getLogger('reactor'); log = jaylog.LogAdapter(logger); handler = jaylog.ColorizingStreamHandler(sys.stdout); formatter = logging.Formatter("%(message)s\n"); handler.setFormatter(formatter); logger.addHandler(handler); logger.setLevel(logging.DEBUG)
"""
class LogAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        super(LogAdapter, self).__init__(logger, {})

    def _get_log_stmt(self, level, msg, *tags, **kwargs):
        frm = inspect.stack()[3]
        mod = inspect.getmodule(frm[0])

        kwargs['pid'] = os.getpid()

        # add message to the payload, substite with the passed data
        kwargs['msg'] = Template(msg).safe_substitute(kwargs)

        kwargs['level'] = logging.getLevelName(level)

        if mod:
            # caller info
            line_no = frm[2]
            method  = frm[3]
            module  = mod.__name__
            loc = kwargs['loc'] = '%s:%s:%s' % (module, method, line_no)

        kwargs['time'] = str(datetime.datetime.now()) # FIXME: custom format

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


class ColorizingStreamHandler(logging.StreamHandler):
    # color names to indices
    COLOR_MAP = {
        'black': 0,
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'magenta': 5,
        'cyan': 6,
        'white': 7,
    }
 
    #levels to (background, foreground, bold/intense)
    LEVEL_MAP = {
        logging.DEBUG: (None, 'blue', False),
        logging.INFO: (None, 'green', False),
        logging.WARNING: (None, 'yellow', False),
        logging.ERROR: (None, 'red', True),
        logging.CRITICAL: ('red', 'red', True),
    }
    csi = '\x1b['
    reset = '\x1b[0m'
 
    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()
 
    def emit(self, record):
        try:
            message = self.format(record)
            stream = self.stream
            if not self.is_tty:
                stream.write(message)
            else:
                self.output_colorized(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
 
    def output_colorized(self, message):
        self.stream.write(message)
 
    def colorize(self, message, record):
        json_rec = json.loads(message)
        
        if record.levelno in self.LEVEL_MAP:
            bg, fg, bold = self.LEVEL_MAP[record.levelno]
            params = []
            if bg in self.COLOR_MAP:
                params.append(str(self.COLOR_MAP[bg] + 40))
            if fg in self.COLOR_MAP:
                params.append(str(self.COLOR_MAP[fg] + 30))
            if bold:
                params.append('1')
            if params:
                if 'level' in json_rec:
                    level = '"level": "%s"' % json_rec['level']
                    color_level = ''.join((self.csi, ';'.join(params), 'm', level, self.reset))
                    message = message.replace(level, color_level)

                if 'msg' in json_rec:
                    msg_str = '"msg": "%s"' % json_rec['msg']
                    color_msg_str = ''.join((self.csi, ';'.join(params), 'm', msg_str, self.reset))
                    message = message.replace(msg_str, color_msg_str)

        for key in json_rec.keys():
            if key in ['msg', 'level']: continue
            # bold the JSON keys
            bg, fg, bold = None, None, True
            params = []
            if bg in self.COLOR_MAP:
                params.append(str(self.COLOR_MAP[bg] + 40))
            if fg in self.COLOR_MAP:
                params.append(str(self.COLOR_MAP[fg] + 30))
            if bold:
                params.append('1')

            val = '"%s":' % key
            color_val = '"' + ''.join((self.csi, ';'.join(params), 'm', key, self.reset)) + '":'
            message = message.replace(val, color_val)

        return message
 
    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            message = message.strip()
            lines = len(message.split('\n'))
            if lines == 1:
                message = self.colorize(message, record)
        return message
