# -*- coding: utf-8 -*-

import os
from unittest import TestCase
from k_util.logger import Logger


class TestLogger(TestCase):

    LOCAL_OUT_FILE = "local_out"
    GLOBAL_OUT_FILE = "global_out"
    ERROR_FILE = "error.log"

    def tearDown(self):
        """ Remove all the artifact files we may have written. """
        if os.path.exists(self.as_log_file(self.LOCAL_OUT_FILE)):
            os.remove(self.as_log_file(self.LOCAL_OUT_FILE))

        if os.path.exists(self.as_log_file(self.GLOBAL_OUT_FILE)):
            os.remove(self.as_log_file(self.GLOBAL_OUT_FILE))

        if os.path.exists(self.ERROR_FILE):
            os.remove(self.ERROR_FILE)

        Logger.clear_actions()

    @staticmethod
    def as_log_file(name: str) -> str:
        return f"{name}.log"

    def test_global_logger(self):
        """ Check that the global (singleton) logger can be initialized and used without error. """
        Logger.log("This is a standard log message.")
        Logger.header("This is a header.")
        Logger.special("This is a special.")
        Logger.field("This is", "a field.")
        Logger.field("This is", "a red field.", red=True)
        Logger.error("This is an error.")

    def test_logging_support(self):
        """ Check that the logging support functions can be called without error. """
        Logger.indent()
        Logger.clear_indent()
        Logger.line_break()
        Logger.unindent()
        Logger.ruler()

    def test_local_logging(self):
        """ Test that we can create a local logging instance that is separate from the singleton. """
        logger = Logger()
        logger.log("This is a message from the local logger.")
        Logger.log("This is a message from the global logger.")
        self.assertNotEqual(logger, Logger.instance())

    def test_file_attach_handler(self):
        """ Test that a file handler can be attached, and that the logger will produce content to it. """

        # Test that we can attach and write to a local output file.
        logger = Logger()
        logger.attach_file_handler(".", self.LOCAL_OUT_FILE)
        logger.log("Hello")
        logger.log("World")
        self.assertTrue(os.path.exists(self.as_log_file(self.LOCAL_OUT_FILE)))

        # Test that we can attach and write to a global output file.
        Logger.attach_file_handler(".", self.GLOBAL_OUT_FILE)
        Logger.log("How are you?")
        self.assertTrue(os.path.exists(self.as_log_file(self.GLOBAL_OUT_FILE)))

        # Test that these two files have the correct line length.
        with open(self.as_log_file(self.LOCAL_OUT_FILE)) as f:
            self.assertEqual(2, len(f.readlines()))

        with open(self.as_log_file(self.GLOBAL_OUT_FILE)) as f:
            self.assertEqual(1, len(f.readlines()))

        # Test error logging.
        Logger.error("This is an error")
        self.assertTrue(os.path.exists(self.ERROR_FILE))
        with open(self.ERROR_FILE) as f:
            self.assertEqual(1, len(f.readlines()))

    def test_log_file_overwrite(self):
        """ Check that attaching a file handler will clear the previous one. """

        # Create the first file.
        logger = Logger()
        logger.attach_file_handler(".", self.LOCAL_OUT_FILE)
        logger.log("1")
        logger.log("2")
        logger.log("3")
        logger.error("e1")
        logger.error("e2")

        # Now the file should be overwritten.
        logger = Logger()
        logger.attach_file_handler(".", self.LOCAL_OUT_FILE)
        logger.log("1")
        logger.error("e1")

        with open(self.as_log_file(self.LOCAL_OUT_FILE)) as f:
            self.assertEqual(1, len(f.readlines()))

        with open(self.ERROR_FILE) as f:
            self.assertEqual(1, len(f.readlines()))

    def test_add_action(self):
        """ Test that we can add an arbitrary action to the global logger. """

        raw_message = "Hello World"

        def my_action(message: str, _: bool):
            self.assertTrue(raw_message in message)

        Logger.add_action("tag", my_action)
        Logger.log(raw_message)

    def test_progress(self):
        """ Simply test if the function can be called. """
        Logger.progress(0.5)
