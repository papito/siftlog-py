import unittest
import json
import logging
from string import Template
from jaylog import LogAdapter

class TestLogger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = LogAdapter(None)

    def test_arbitrary_constants(self):
        logger = LogAdapter(None, pid=12345, app='APP NAME')
        res = json.loads(logger._get_log_stmt(logging.INFO, None))
        
        self.assertEquals(res['pid'], 12345)
        self.assertEquals(res['app'], 'APP NAME')

    def test_simple_log_statement(self):
        stmt = 'simple log statement'
        res = json.loads(self.logger._get_log_stmt(logging.DEBUG, stmt))

        self.assertEquals(res['msg'], stmt)
    
    def test_with_string_formatting(self):
        stmt = 'simple log statement with variable $var'
        data = {'var': 1}
        res = json.loads(self.logger._get_log_stmt(logging.DEBUG, stmt, **data))

        self.assertEquals(res['msg'], Template(stmt).substitute(data))
        
    def test_tags(self):
        data = {}
        res = self.logger._get_log_stmt(logging.DEBUG, '', 'TAG1', 'TAG2')
        res = json.loads(res)

        self.assertEquals(len(res['tags']), 2)
