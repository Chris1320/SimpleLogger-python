"""
MIT License

Copyright (c) 2020-2022 Chris1320

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os

if os.path.exists("logfile.log"):
    os.remove("logfile.log")

if os.path.exists("logfile2.log"):
    os.remove("logfile2.log")


from simplelogger.logger import Logger


class TestClass():
    def test_logging(self):
        logger = Logger("Test Logger", "logfile.log", loglevel=5)
        for i in range(1, 1001):
            logger.info(f"Logging test #{i}")

        for i in range(1, 1001):
            logger.debug(f"Logging test #{i}")

        for i in range(1, 1001):
            logger.warning(f"Logging test #{i}")

        for i in range(1, 1001):
            logger.error(f"Logging test #{i}")

        for i in range(1, 1001):
            logger.critical(f"Logging test #{i}")

        assert logger.getLoggerInfo()["stats"]["log_size"] == 5000

    def test_memory_mode(self):
        logger = Logger("Test Logger (Memory Mode)", "logfile2.log", loglevel=5, memory=True, mode="overwrite")
        for i in range(1, 1001):
            logger.info(f"Memory Logging test #{i}")

        for i in range(1, 1001):
            logger.debug(f"Memory Logging test #{i}")

        for i in range(1, 1001):
            logger.warning(f"Memory Logging test #{i}")

        for i in range(1, 1001):
            logger.error(f"Memory Logging test #{i}")

        for i in range(1, 1001):
            logger.critical(f"Memory Logging test #{i}")

        logger.dumpLogs()

    def test_default_logging(self):
        logger = Logger("Test Logger", "logfile.log")
        logger.debug("Default Logging test")
        logger.info("Default Logging test")
        logger.warning("Default Logging test")
        logger.error("Default Logging test")
        logger.critical("Default Logging test")

        assert logger.getLoggerInfo()["stats"]["log_size"] == 3
        for log in logger.getAllLogs():
            assert log["type"] in ["warning", "error", "critical"]

    def test_autoforget(self):
        logger = Logger("Logfile Size Limit Test Logger", "logfile.log", loglevel=5, logsize=50, autoforget=True)
        for i in range(1, 51):
            logger.info(f"Autoforget Logging test #{i}")

        assert len(logger.getAllLogs()) == 50
        assert logger.getLoggerInfo()["stats"]["log_size"] == 50

        for i in range(1, 26):
            logger.info(f"More Logging test #{i}")

        assert len(logger.getAllLogs()) == 50
        assert logger.getLoggerInfo()["stats"]["log_size"] == 50
