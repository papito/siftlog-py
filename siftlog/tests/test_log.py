import datetime
import json
import logging
import unittest
from string import Template

from siftlog import SiftLog


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core_logger = logging.getLogger("siftlog_test")
        cls.sift_logger = SiftLog(cls.core_logger)

    def test_arbitrary_constants(self):
        logger = SiftLog(self.core_logger, pid=12345, app="APP NAME")
        res = json.loads(logger._get_log_stmt(logging.INFO, None))

        self.assertEquals(res["pid"], 12345)
        self.assertEquals(res["app"], "APP NAME")

    def test_arbitrary_dynamic_constants(self):
        func = lambda: "FUNC_RESULT"

        logger = SiftLog(self.core_logger, pid=12345, app="APP NAME", func=func)

        res = json.loads(logger._get_log_stmt(logging.INFO, None))

        self.assertEquals(res["pid"], 12345)
        self.assertEquals(res["app"], "APP NAME")
        self.assertEquals(res["func"], "FUNC_RESULT")

    def test_simple_log_statement(self):
        stmt = "simple log statement"
        res = json.loads(self.sift_logger._get_log_stmt(logging.DEBUG, stmt))

        self.assertEquals(res[self.sift_logger.MESSAGE], stmt)

    def test_with_string_formatting(self):
        stmt = "simple log statement with variable $var"
        data = {"var": 1}
        res = json.loads(self.sift_logger._get_log_stmt(logging.DEBUG, stmt, **data))

        self.assertEquals(
            res[self.sift_logger.MESSAGE], Template(stmt).substitute(data)
        )

    def test_tags(self):
        res = self.sift_logger._get_log_stmt(logging.DEBUG, "", "TAG1", "TAG2")
        res = json.loads(res)

        self.assertEquals(len(res[self.sift_logger.TAGS]), 2)

    def test_custom_adapter(self):
        def datetime_handler(obj):

            if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
                return obj.isoformat()
            else:
                return None

        class CustomAdapter(SiftLog):
            def to_json(self, data):
                return json.dumps(data, default=datetime_handler)

        test_logger = logging.getLogger("siftlog_test")
        logger = CustomAdapter(test_logger)

        res = logger._get_log_stmt(
            logging.DEBUG, "$created", created=datetime.datetime.now()
        )
        res = json.loads(res)
        self.assertNotEquals(res[logger.LEVEL], "ERROR")

    def test_core_fields(self):
        test_logger = logging.getLogger("siftlog_test")
        logger = SiftLog(test_logger)
        logger.MESSAGE = "m"
        logger.LEVEL = "l"
        res = logger._get_log_stmt(logging.DEBUG, "")
        res = json.loads(res)
        self.assertTrue(logger.MESSAGE in res)
        self.assertTrue(logger.MESSAGE in res)
        self.assertTrue(logger.LOCATION in res)
