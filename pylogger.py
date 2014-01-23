import time
import os
from datetime import datetime

# PyLogger log format:
# {message}
# {logtype}
# {timestamp}
class PyLogger():
    def __init__(self,filename='pylogger.log',
                      defaultlogtype='INFO',
                      logformat='[{timestamp}] {logtype}: {message}',
                      timestamp='%Y-%m-%d %H:%M:%S',
                      prefix='',
                      postfix='\n'):
        self.fileName = filename
        self.logType = defaultlogtype
        self.logFormat = logformat
        self.timeStamp = timestamp
        self.postfix = postfix
        self.prefix = prefix
        self.disabled = False

    def open(self,*args):
        self.__init__(*args)
        self.clear()

    def clear(self):
        try:
            open(self.fileName,'w').close()
        except IOError, e:
            raise Exception("Could not clear log file: {0}\nDetails: {1}".format(self.fileName,e))
    def delete(self):
        try:
            if os.path.isfile(self.fileName):
                os.remove(self.fileName)
        except OSError, e:
            raise Exception("Could not delete log file: {0}\nDetails: {1}".format(self.fileName,e))

    def pause(self):
        self.disabled = True

    def isPaused(self):
        return self.disabled

    def resume(self):
        self.disabled = False

    def setLogType(self,logtype):
        self.logType = logtype

    def resetLogFormat(self):
        self.logFormat='[{timestamp}]{logtype}: {message}'

    def setLogFormat(self,logformat):
        self.logFormat = logformat

    def resetTimestampFormat(self):
        self.timeStamp = '%Y-%m-%d %H:%M:%S'

    def setTimestampFormat(self,timestamp):
        self.timeStamp = timestamp

    def getTimeStamp(self):
        if self.timeStamp != None and len(self.timeStamp) > 2:
            ts = datetime.fromtimestamp(time.time()).strftime(self.timeStamp)
            return ts
        else:
            return ''

    def createIfNonExistent(self):
        if not os.path.isfile(self.fileName):
            self.clear()

    def log(self,logstr,logtype=''):
        if self.disabled:
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
        except IOError, e:
            raise Exception("Could not save log file: {0}\nDetails: {1}".format(self.fileName,e))

    def info(self,logstr):
        self.log(logstr,"INFO")
        
    def warning(self,logstr):
        self.log(logstr,"WARNING")

    def error(self,logstr):
        self.log(logstr,"ERROR")

    def critical(self,logstr):
        self.log(logstr,"CRITICAL")

    def exception(self,logstr):
        self.log(logstr,"EXCEPTION")
