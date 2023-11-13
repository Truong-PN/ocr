import logging
import os
from datetime import date

from unidecode import unidecode
from django.conf import settings

class Logger:
    def __init__(self,
        currentFile=__file__,
        filename : str = "autobot.%Y.%m.%d.log",
        clear : bool = False,
        console : bool = False):
        """
            Auto create directory with date time and unicode message log

            *Params:
                currentFile: to add path file running in log message
                filename : default format file name
                clear: to clear data of log file
                console: to print in console
            *Methods:
                info: log info
                warning: log warning
                error: log error
        """
        today = date.today()
        logName = today.strftime(filename)

        self.__file__ = os.path.abspath(os.path.normpath(currentFile))
        self.logDir = settings.LOG_ROOT
        self.logFile = os.path.join(self.logDir, logName)
        self.log = logging
        self.console = console
        if clear or not os.path.exists(self.logFile):
            self.clear()
        logging.basicConfig(
            format=f"[%(asctime)s] - %(levelname)-6s: ['{self.__file__}'] - %(message)s",
            filename=self.logFile,
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True
        )
        logging.raiseExceptions = False

    def clear(self):
        with open(self.logFile, "w"):
            pass

    def info(self, msg):
        self.log.info(f"{unidecode(msg)}")
        if self.console:
            print(f"INFO: {unidecode(msg)}")

    def warning(self, msg):
        self.log.warning(f"{unidecode(msg)}")
        if self.console:
            print(f"WARNING: {unidecode(msg)}")

    def error(self, msg):
        self.log.error(f"{unidecode(msg)}")
        if self.console:
            print(f"ERROR: {unidecode(msg)}")
