import unittest
import sys
import logging
from siftlog import SiftLog, ColorStreamHandler

class TestColor(unittest.TestCase):

    def test_defaults(self):
        logger = logging.getLogger()
        logger.setLevel(logging.TRACE)
        handler = ColorStreamHandler(sys.stdout)
        logger.addHandler(handler)
        log = SiftLog(logger)
        
        log.trace('trace', 'tag1', 'tag2', key1='key1', key2='key2')
        log.debug('debug', 'tag1', 'tag2', key1='key1', key2='key2')
        log.info('info', 'tag1', 'tag2', key1='key1', key2='key2')
        log.warn('warn', 'tag1', 'tag2', key1='key1', key2='key2')
        log.warning('warning', 'tag1', 'tag2', key1='key1', key2='key2')
        log.critical('critical', 'tag1', 'tag2', key1='key1', key2='key2')

    def test_changed_key_names(self):
        logger = logging.getLogger()
        logger.setLevel(logging.TRACE)
        handler = ColorStreamHandler(sys.stdout)
        logger.addHandler(handler)
        log = SiftLog(logger)
        SiftLog.MESSAGE = 'm'
        SiftLog.LOC = 'from'
        SiftLog.LEVEL = 'lvl'
        SiftLog.TIME = '@'
        SiftLog.TAGS = 't'
        
        log.trace('trace', 'tag1', 'tag2', key1='key1', key2='key2')
        log.debug('debug', 'tag1', 'tag2', key1='key1', key2='key2')
        log.info('info', 'tag1', 'tag2', key1='key1', key2='key2')
        log.warn('warn', 'tag1', 'tag2', key1='key1', key2='key2')
        log.warning('warning', 'tag1', 'tag2', key1='key1', key2='key2')
        log.critical('critical', 'tag1', 'tag2', key1='key1', key2='key2')
