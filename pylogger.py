
"""

PyLogger

PyLogger is a simple data to file logging module. 
Use it to quickly log and debug scripts without sacrificing 
precious space in your script. Log events, warnings, exceptions 
and more into a readable log file with a customizable output!

"""


import time
import os
from datetime import datetime

__version__ = '0.1'


class PyLogger():
    """The PyLogger class"""

    def __init__(self,filename='pylogger.log',
                      defaultlogtype='INFO',
                      logformat='[{timestamp}] {logtype}: {message}',
                      timestamp='%Y-%m-%d %H:%M:%S',
                      prefix='',
                      postfix='\n'):

        """Initialize a PyLogger object.

            :param filename: The filename to use
            :type filename: str
            :param defaultlogtype: Initial log type to use [INFO]
            :type defaultlogtype: str
            :param timestamp: Initial timestamp format [%Y-%m-%d %H:%M:%S]
            :type timestamp: str
            :param prefix: String to insert before the log message
            :type prefix: str
            :param postfix: String to append to the log message
            :type postfix: str

        """
        self.fileName = filename
        self.logType = defaultlogtype
        self.logFormat = logformat
        self.timeStamp = timestamp
        self.postfix = postfix
        self.prefix = prefix
        self.enabled = False

    def open(self,*args):
        """Initialize a new logger"""
        self.__init__(*args)

    def clear(self):
        """Clear the content of the log file

            :returns: True -- file cleared
            :raises: IOError, Exception

        """
        try:
            open(self.fileName,'w').close()
            return True
        except IOError, e:
            raise Exception("Could not clear log file: {0}\nInfo: {1}".format(self.fileName,e))

    def delete(self):
        """Delete the log file

            :returns: True -- file deleted
            :raises: OSError, Exception

        """
        try:
            if os.path.isfile(self.fileName):
                os.remove(self.fileName)
        except OSError, e:
            raise Exception("Could not delete log file: {0}\nInfo: {1}".format(self.fileName,e))

    def pause(self):
        """Pause the logging until resumed"""
        self.enabled = False

    def isEnabled(self):
        """Check if enabled/paused

            :returns: True -- enabled

        """
        return self.enabled

    def resume(self):
        """Resume the logging from paused"""
        self.enabled = True

    def setLogType(self,logtype):
        """Set the log type

            :param logtype: Log type
            :type logtype: str

        """
        self.logType = logtype

    def setLogFormat(self,logformat):
        """Set custom log format

            :param logformat: Log format
                Available options: {timestamp}, {logtype}, {message}
                Example: [{timestamp}]{logtype}: {message}
            :type logformat: str

        """
        self.logFormat = logformat

    def resetLogFormat(self):
        """Reset log format to default format"""
        self.logFormat='[{timestamp}]{logtype}: {message}'

    def setTimestampFormat(self,timestamp):
        """Set custom timestamp format

            :param timestamp: Timestamp
                Example: %Y-%m-%d %H:%M:%S
            :type timestamp: str

        """
        self.timeStamp = timestamp

    def resetTimestampFormat(self):
        """Reset timestamp format"""
        self.timeStamp = '%Y-%m-%d %H:%M:%S'

    def getTimeStamp(self):
        """Function to get the current time, returns in the timestamp format

            :returns: Timestamp string

        """
        if len(self.timeStamp) >= 2:
            ts = datetime.fromtimestamp(time.time()).strftime(self.timeStamp)
            return ts
        else:
            return ''

    def createIfNonExistent(self):
        """Create an empty log file if non existant

            :returns: True -- file cleared
            :raises: IOError, Exception

        """
        if not os.path.isfile(self.fileName):
            return self.clear()

    def log(self,logstr,logtype=''):
        """Function to log message to file.

            :param logstr: The string you want to log
            :type logstr: str
            :param logtype: Optional argument, custom log type. 
                If not provided, defaults to defined log type.
            :type logtype: str

            :returns: True -- String has been logged to file
            :raises: IOError,Exception7

        """
        if not self.enabled:
            return False
        try:
            self.createIfNonExistent()
            
            cLogType = self.logType
            if logtype != '':
                cLogType = logtype

            logMessage = self.logFormat.format(timestamp=self.getTimeStamp(),
                                               logtype=cLogType,
                                               message=logstr)
            with open(self.fileName,'a') as f:
                f.write(self.prefix + logMessage + self.postfix)
                f.close()
            return True
        except IOError, e:
            raise Exception("Could not save log file: {0}\nDetails: {1}".format(self.fileName,e))

    def info(self,logstr):
        """Function that calls the log function with type INFO"""
        self.log(logstr,"INFO")

    def warning(self,logstr):
        """Function that calls the log function with type WARNING"""
        self.log(logstr,"WARNING")

    def error(self,logstr):
        """Function that calls the log function with type ERROR"""
        self.log(logstr,"ERROR")

    def critical(self,logstr):
        """Function that calls the log function with type CRITICAL"""
        self.log(logstr,"CRITICAL")

    def exception(self,logstr):
        """Function that calls the log function with type EXCEPTION"""
        self.log(logstr,"EXCEPTION")
