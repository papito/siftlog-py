import logging
import sys
import unittest

from siftlog import ColorStreamHandler, SiftLog


class TestColor(unittest.TestCase):
    def test_defaults(self):
        logger = logging.getLogger()
        logger.setLevel(logging.TRACE)
        handler = ColorStreamHandler(sys.stdout)
        logger.addHandler(handler)
        log = SiftLog(logger)

        log.trace("trace", "tag1", "tag2", key1="key1", key2="key2")
        log.debug("debug", "tag1", "tag2", key1="key1", key2="key2")
        log.info("info", "tag1", "tag2", key1="key1", key2="key2")
        log.warn("warn", "tag1", "tag2", key1="key1", key2="key2")
        log.warning("warning", "tag1", "tag2", key1="key1", key2="key2")
        log.critical("critical", "tag1", "tag2", key1="key1", key2="key2")

    def test_changed_key_names(self):
        logger = logging.getLogger()
        logger.setLevel(logging.TRACE)
        handler = ColorStreamHandler(sys.stdout)
        logger.addHandler(handler)
        log = SiftLog(logger)
        SiftLog.MESSAGE = "m"
        SiftLog.LOC = "from"
        SiftLog.LEVEL = "lvl"
        SiftLog.TIME = "@"
        SiftLog.TAGS = "t"

        log.trace("trace", "tag1", "tag2", key1="key1", key2="key2")
        log.debug("debug", "tag1", "tag2", key1="key1", key2="key2")
        log.info("info", "tag1", "tag2", key1="key1", key2="key2")
        log.warn("warn", "tag1", "tag2", key1="key1", key2="key2")
        log.warning("warning", "tag1", "tag2", key1="key1", key2="key2")
        log.critical("critical", "tag1", "tag2", key1="key1", key2="key2")

    def test_incorrect_usage(self):
        handler = ColorStreamHandler(sys.stdout)

        with self.assertRaises(RuntimeError) as cm:
            handler.set_color("blah", bg=handler.GREEN, fg=handler.WHITE, bold=True)
        with self.assertRaises(RuntimeError) as cm:
            handler.set_color(logging.INFO, bg="bad", fg=handler.WHITE, bold=True)
        with self.assertRaises(RuntimeError) as cm:
            handler.set_color(logging.INFO, bg=handler.BLACK, fg="bad", bold=True)
        with self.assertRaises(RuntimeError) as cm:
            handler.set_color(
                logging.INFO, bg=handler.BLACK, fg=handler.WHITE, bold="bad"
            )

    def test_correct_usage(self):
        handler = ColorStreamHandler(sys.stdout)

        handler.set_color(logging.INFO, bg=handler.GREEN, fg=handler.WHITE, bold=True)
        handler.set_color(logging.TRACE, bg=handler.CYAN, fg=handler.RED, bold=False)
        handler.set_color(logging.DEBUG, bg=handler.WHITE, fg=handler.BLUE, bold=True)

        logger = logging.getLogger()
        logger.setLevel(logging.TRACE)
        logger.addHandler(handler)
        log = SiftLog(logger)

        log.trace("trace", "tag1", "tag2", key1="key1", key2="key2")
        log.debug("debug", "tag1", "tag2", key1="key1", key2="key2")
        log.info("info", "tag1", "tag2", key1="key1", key2="key2")
