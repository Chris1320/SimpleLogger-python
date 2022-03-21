"""
MIT License

Copyright (c) 2022 Chris1320

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
import logging


class Logger():
    """
    The logger class.
    """

    def __init__(self, name: str, logfile: str, **kwargs):
        """
        The initialization method of the Logger() class.

        name: str, The name of the logging object.
        logfile: str, the path where to write the logs.
        kwargs: dict, The keyword arguments.
            mode: bool, set to the following modes: (Default: `append`)
                append: Append logs to existing file.
                overwrite: Overwrite existing file.
            memory: If True, store logs in memory and manually call `dump()` to dump to file. (Default: False)
        """

        self.name = str(name)
        self.mode = kwargs.get(mode, "append") if kwargs.get(mode, "append") in ("append", "overwrite") else raise ValueError("mode must be `append` or `overwrite`.")
        self.memory = kwargs.get(memory, False)

