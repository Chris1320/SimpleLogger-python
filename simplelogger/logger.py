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

import logging


class Logger:
    __initialized: bool = False  # True if handlers are already added to the logger.

    def __init__(
        self,
        logfilepath: str,
        logformat: str = "%(asctime)s|%(levelname)s|%(module)s at line %(lineno)s| %(message)s",
        force_debug: bool = False
    ):
        """
        Initialize the logger.

        :param logfilepath: The path of the file to store log files to.
        :param logformat: The format of the logs.
        :param force_debug: Force-enable debug mode.
        """

        # Initialize the logger, file handler, and formatter.
        self.__logger = logging.getLogger(__name__)
        if not self.__initialized:
            _FileHandler = logging.FileHandler(logfilepath)
            _Formatter = logging.Formatter(logformat)

            _FileHandler.setFormatter(_Formatter)  # Add the formatter to the file handler.
            self.__logger.addHandler(_FileHandler)  # Add the file handler to the logger.

            self.__logger.setLevel(logging.DEBUG if force_debug else logging.WARNING)
            Logger.__initialized = True

    def __call__(self) -> logging.Logger:
        """
        Get the logger object.
        """

        return self.__logger

    def __repr__(self) -> str:
        return self.__logger.__repr__()
