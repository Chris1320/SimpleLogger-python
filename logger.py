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

        :**kwargs str name: Name of the logging object.
        :**kwargs int session_id: Session ID of the logging object.
        :**kwargs str logfile: Path of logfile to write data into.
        :**kwargs tuple funcs: A list/tuple of function objects that
                               accepts the following kwargs:
            - name
            - session_id
            - logfile
            - message
            - mtype
                               The functions in the list are called
                               after logging the messages.
        """

        self.VERSION = [0, 0, 1, 2]

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

        # Set the tuple of functions to call after
        self.afterlog_funcs = kwargs.get('funcs', ())

    def _write(self, message):
        """
        Write data into a logfile.

        :param str message: The message to write.

        :returns void:
        """

        # I didn't put a try/except block to let
        # the user to customize it.

        if self.logfile is None:
            return None

        else:
            with open(self.logfile, 'a') as fopen:
                fopen.write(message)
                fopen.write('\n')

    def _format(self, message, logtype, caller):
        """
        Format the message into a more informative one.

        :param str message: Log message
        :param str logtype: The log message type.
        :param str caller: The name of the function that called the logger.

        :returns str: The newer version of the message.
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
        Return the log data in a form of tuple in a list.

        :returns tuple: The log data in tuple in a list form.
        """

        return self.log_datas

    def get_log_data(self, log_number):
        """
        Get a specific log data.

        :param int log_number: The index number to get the data of log number.

        :returns str: Return the content of the specified log number.
        """

        return self.log_datas[log_number]

    def get_latest_log_data(self):
        """
        Return the last message recieved by logger.

        :returns str: The last message recieved by the logger.
        """

        return self.log_data

    def set_logging_level(self, level):
        """
        Set logging level.

        :returns void:
        """

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
        Show logging information.

        :returns void:
        """

        if self.level is None:
            raise self.LevelNotSetError("Logging level is not yet defined! Run `logger.LoggingObject().set_logging_level([LEVEL])` to set the level.")

        else:
            # logging.basicConfig(level=self.level)
            self.print_logs = True

    def _call_funcs(self, message, mtype):
        """
        Call the functions passed by the user.

        :param str message: The message to log.
        :param str mtype: The log message type.

        :returns void:
        """

        for function in self.afterlog_funcs:
            try:
                function(
                    name=self.name,
                    session_id=self.session_id,
                    logfile=self.logfile,
                    message=message,
                    mtype=mtype
                )

            except Exception as e:
                pass

    def info(self, message):
        """
        Log information.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'info', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'info'))
        self.log_data = (message, 'info')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'info')

    def warning(self, message):
        """
        Log warnings.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'warning', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'warning'))
        self.log_data = (message, 'warning')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'warning')

    def error(self, message):
        """
        Log errors.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'error', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'error'))
        self.log_data = (message, 'error')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'error')

    def debug(self, message):
        """
        Log debugging information.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'debug', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'debug'))
        self.log_data = (message, 'debug')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'debug')

    def critical(self, message):
        """
        Log critical errors.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'critical', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'critical'))
        self.log_data = (message, 'critical')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'critical')

    class LevelNotSetError(Exception):
        """
        An exception class.
        """

        pass
