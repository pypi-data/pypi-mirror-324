# Part of libunn, view: https://github.com/juanvel4000/libunn
import os
from datetime import datetime
class Log:
    def __init__(self, logfile):
        self.logfile = logfile
        with open(logfile, 'w') as logfile:
            logfile.write(f"{self.getTimestamp()} {self.getLevel(0)}: LOG STARTED\n")
    def getTimestamp():
        return datetime.now().isoformat()
    def getLevel(level):
        levels = {
            "5": "FATAL",
            "1": "SUCCESS",
            "4": "ERROR",
            "3": "WARNING",
            "2": "OK",
            "0": "INFO"
        }
        return levels[level]
    def Fatal(self, message):
        with open(self.logfile, 'a') as lf:
            lf.write(f"{self.getTimestamp()} [{self.getLevel(5)}] {message}\n")
            return True
    def Error(self, message):
        with open(self.logfile, 'a') as lf:
            lf.write(f"{self.getTimestamp()} [{self.getLevel(4)}] {message}\n")
            return True
    def Warn(self, message):
        with open(self.logfile, 'a') as lf:
            lf.write(f"{self.getTimestamp()} [{self.getLevel(3)}] {message}\n")
            return True
    def OK(self, message):
        with open(self.logfile, 'a') as lf:
            lf.write(f"{self.getTimestamp()} [{self.getLevel(2)}] {message}\n")
            return True
    def Success(self, message):
        with open(self.logfile, 'a') as lf:
            lf.write(f"{self.getTimestamp()} [{self.getLevel(1)}] {message}\n")
            return True
    def Info(self, message):
        with open(self.logfile, 'a') as lf:
            lf.write(f"{self.getTimestamp()} [{self.getLevel(0)}] {message}\n")
            return True