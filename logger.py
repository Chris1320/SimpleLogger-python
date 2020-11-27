# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 Chris1320

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

import sys
import time
import random
import logging

"""
Wrapper module for logging

Basic Usage:
    ```
    import logger

    # Get a logging object.
    log_obj = logger.LoggingObject(
        name='SampleLogger',
        logfile='logfile.log'
        )

    # Set the log level to show.
    log_obj.set_logging_level('NOTSET')

    # Show logs in the screen.
    log_obj.enable_logging()

    log_obj.info("Sample Information message.")
    log_obj.warning("Sample warning message.")
    log_obj.error("Sample error message.")
    log_obj.debug("Sample debug message.")
    log_obj.critical("Sample critical message.")
    ```
"""


class LoggingObject:
    """
    The main class of Logger.
    """

    def __init__(self, **kwargs):
        """
        Initialization method of the logging object.

        :**kwargs name: Name of the logging object.
        :**kwargs session_id: Session ID of the logging object.
        :**kwargs logfile: Path of logfile to write data into.
        """

        self.VERSION = [0, 0, 1, 1]

        # Set the name of the logger.
        self.name = kwargs.get('name', __name__)

        # Set the session ID of the logger.
        rand_id = random.randint(100000, 999999)
        self.session_id = kwargs.get('session_id', rand_id)
        del rand_id

        # Set the path of the logfile to write data into.
        self.logfile = kwargs.get('logfile', None)

        # Initialize the main logging object.
        self.logger = logging.getLogger(self.name)

        # Set the logging level.
        self.level = None

        # Set the value of print_logs
        self.print_logs = False

        # Set the time when the logger has started.
        self.start_time = time.asctime()

        # Set the current data
        self.log_datas = []  # All logs inf dict form {log_type:  message}
        self.log_data = ""  # Current/Latest log

    def _write(self, message):
        """
        def _write():
            Write data into a logfile.
        """

        # I didn't put a try/except block to let
        # the user to customize it.

        if self.logfile is None:
            return None

        else:
            with open(self.logfile, 'a') as fopen:
                fopen.write(message + '\n')

    def _format(self, message, logtype, caller):
        """
        def _format():
            Format the message into a more informative one.

            :param message: Log message
        """

        if str(caller) == "<module>":
            pass

        else:
            caller = str(caller) + "()"

        result = ":{}: [{}] ({}) | {} | {}".format(
                logtype.upper(),
                str(self.session_id),
                time.strftime("%H:%M:%S %b %d %Y"),
                caller,
                message
                )

        # I put this here because I'm lazy doing another method.
        if self.print_logs == True:
            print(result)

        return result

    def get_all_log_datas(self):
        """
        def get_all_log_datas():
            Return the log data in a form of tuple in a list.
        """

        return self.log_datas

    def get_log_data(self, log_number):
        """
        def get_log_data():
            Get a specific log data.

            :param log_number: The index number to get the data of log number.
            :type int:

            :returns: Return the content of the specified log number.
            :return type: str
        """

        return self.log_datas[log_number]

    def get_latest_log_data(self):
        """
        def get_latest_log_data():
            Return the last message recieved by logger.
        """

        return self.log_data

    def set_logging_level(self, level):
        if level.upper() == "NOTSET":
            self.level = "NOTSET"

        elif level.upper() == "INFO":
            self.level = "INFO"

        elif level.upper() == "WARNING":
            self.level = "WARNING"

        elif level.upper() == "ERROR":
            self.level = "ERROR"

        elif level.upper() == "DEBUG":
            self.level = "DEBUG"

        elif level.upper() == "CRITICAL":
            self.level = "CRITICAL"

        else:
            raise ValueError("argument `level` must be `NOTSET`, `INFO`, `WARNING`, `ERROR`, `DEBUG`, or `CRITICAL`!")

    def enable_logging(self):
        """
        def enable_logging():
            Show logging information.
        """

        if self.level is None:
            raise self.LevelNotSetError("Logging level is not yet defined! Run `logger.LoggingObject().set_logging_level([LEVEL])` to set the level.")

        else:
            # logging.basicConfig(level=self.level)
            self.print_logs = True

    def info(self, message):
        """
        def info():
            Log information.

            :param message: Log message.
        """

        message = self._format(message, 'info', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'info'))
        self.log_data = (message, 'info')
        self.logger.info(message)
        self._write(message)

    def warning(self, message):
        """
        def warning():
            Log warnings.

            :param message: Log message.
        """

        message = self._format(message, 'warning', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'warning'))
        self.log_data = (message, 'warning')
        self.logger.info(message)
        self._write(message)

    def error(self, message):
        """
        def error():
            Log errors.

            :param message: Log message.
        """

        message = self._format(message, 'error', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'error'))
        self.log_data = (message, 'error')
        self.logger.info(message)
        self._write(message)

    def debug(self, message):
        """
        def debug():
            Log debugging information.

            :param message: Log message.
        """

        message = self._format(message, 'debug', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'debug'))
        self.log_data = (message, 'debug')
        self.logger.info(message)
        self._write(message)

    def critical(self, message):
        """
        def critical():
            Log critical errors.

            :param message: Log message.
        """

        message = self._format(message, 'critical', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'critical'))
        self.log_data = (message, 'critical')
        self.logger.info(message)
        self._write(message)

    class LevelNotSetError(Exception):
        """
        class LevelNotSetError():
            An exception class.
        """

        pass
