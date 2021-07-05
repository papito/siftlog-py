import datetime
import json
import logging
import unittest
from string import Template

from siftlog import SiftLog


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = SiftLog(None)

    def test_arbitrary_constants(self):
        logger = SiftLog(None, pid=12345, app="APP NAME")
        res = json.loads(logger._get_log_stmt(logging.INFO, None))

        self.assertEquals(res["pid"], 12345)
        self.assertEquals(res["app"], "APP NAME")

    def test_simple_log_statement(self):
        stmt = "simple log statement"
        res = json.loads(self.logger._get_log_stmt(logging.DEBUG, stmt))

        self.assertEquals(res[self.logger.MESSAGE], stmt)

    def test_with_string_formatting(self):
        stmt = "simple log statement with variable $var"
        data = {"var": 1}
        res = json.loads(self.logger._get_log_stmt(logging.DEBUG, stmt, **data))

        self.assertEquals(res[self.logger.MESSAGE], Template(stmt).substitute(data))

    def test_tags(self):
        res = self.logger._get_log_stmt(logging.DEBUG, "", "TAG1", "TAG2")
        res = json.loads(res)

        self.assertEquals(len(res[self.logger.TAGS]), 2)

    def test_custom_adapter(self):
        datetime_handler = lambda obj: (
            obj.isoformat()
            if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date)
            else None
        )

        class CustomAdapter(SiftLog):
            def to_json(self, data):
                return json.dumps(data, default=datetime_handler)

        logger = CustomAdapter(None)

        res = logger._get_log_stmt(
            logging.DEBUG, "$created", created=datetime.datetime.now()
        )
        res = json.loads(res)
        self.assertNotEquals(res[logger.LEVEL], "ERROR")

    def test_core_fields(self):
        logger = SiftLog(None)
        logger.MESSAGE = "m"
        logger.LEVEL = "l"
        res = logger._get_log_stmt(logging.DEBUG, "")
        res = json.loads(res)
        self.assertTrue(logger.MESSAGE in res)
        self.assertTrue(logger.LEVEL in res)
