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
    LOCATION_FORMAT = '$module:$method:$line_no'

    def __init__(self, logger, **kwargs):
        super(SiftLog, self).__init__(logger, {})
        self._constants   = kwargs

    def _get_log_stmt(self, level, msg, *tags, **kwargs):
        msg = msg or ''

        kwargs[self.LEVEL] = logging.getLevelName(level)

        # append the optional constants defined on initialization
        kwargs.update(self._constants)

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
        caller = self._get_caller_info()

        if not caller:
            return None

        return Template(self.LOCATION_FORMAT).safe_substitute(caller)

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
        
        return {
            'file': frm[1],
            'line_no' : frm[2],
            'method'  : frm[3],
            'module'  : mod.__name__,
        }

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


class ColorStreamHandler(logging.StreamHandler):
    """
        This is  modeled after https://gist.github.com/vsajip/758430
    """

    BLACK   = 'black'
    RED     = 'red'
    GREEN   = 'green'
    YELLOW  = 'yellow'
    BLUE    = 'blue'
    MAGENTA = 'magenta'
    CYAN    = 'cyan'
    WHITE   = 'white'

    # color names to indices
    _COLOR_MAP = {
        BLACK: 0,
        RED: 1,
        GREEN: 2,
        YELLOW: 3,
        BLUE: 4,
        MAGENTA: 5,
        CYAN: 6,
        WHITE: 7,
    }
 
    # levels to (background, foreground, bold/intense)
    _LEVEL_MAP = {
        logging.TRACE: (None, None, False),
        logging.DEBUG: (None, BLUE, False),
        logging.INFO: (None, GREEN, False),
        logging.WARNING: (None, YELLOW, False),
        logging.ERROR: (None, RED, True),
        logging.CRITICAL: (RED, WHITE, True),
    }

    @staticmethod
    def set_color(level=None, bg=None, fg=None, bold=False):
        assert level
        
        if level not in ColorStreamHandler._LEVEL_MAP:
            raise RuntimeError('Logging level "{}" is invalid'.format(level))

        if bg and bg not in ColorStreamHandler._COLOR_MAP:
            raise RuntimeError('Background color "{}" is invalid'.format(bg))

        if fg and fg not in ColorStreamHandler._COLOR_MAP:
            raise RuntimeError('Foreground color "{}" is invalid'.format(fg))

        if not isinstance(bold, bool):
            raise RuntimeError('Bold flag must be a True/False')
        
        ColorStreamHandler._LEVEL_MAP[level] = (bg, fg, bold)
    
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
            if os.name != 'posix' or not self.is_tty:
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
        
        if record.levelno in self._LEVEL_MAP:
            bg, fg, bold = self._LEVEL_MAP[record.levelno]
            params = []
            if bg in self._COLOR_MAP:
                params.append(str(self._COLOR_MAP[bg] + 40))
            if fg in self._COLOR_MAP:
                params.append(str(self._COLOR_MAP[fg] + 30))
            if bold:
                params.append('1')
            if params:
                if SiftLog.LEVEL in json_rec:
                    level = '"{0}": "{1}"'.format(SiftLog.LEVEL, json_rec[SiftLog.LEVEL])
                    color_level = ''.join((self.csi, ';'.join(params), 'm', level, self.reset))
                    message = message.replace(level, color_level)

                if SiftLog.MESSAGE in json_rec:
                    msg = '"{0}": "{1}"'.format(SiftLog.MESSAGE, json_rec[SiftLog.MESSAGE])
                    color_msg = ''.join((self.csi, ';'.join(params), 'm', msg, self.reset))
                    message = message.replace(msg, color_msg)

        for key in json_rec.keys():
            if key in [SiftLog.MESSAGE, SiftLog.LEVEL]: continue
            # bold the JSON keys
            bg, fg, bold = None, None, True
            params = []
            if bg in self._COLOR_MAP:
                params.append(str(self._COLOR_MAP[bg] + 40))
            if fg in self._COLOR_MAP:
                params.append(str(self._COLOR_MAP[fg] + 30))
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

