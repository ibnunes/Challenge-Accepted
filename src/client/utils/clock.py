import time

class Clock:
    @staticmethod
    def now():
        return int(time.time())

    @staticmethod
    def isAfter(date_curr, date_next):
        if (date_curr is None) or (date_next is None):
            return False
        return date_curr > date_next

    @staticmethod
    def addSeconds(date_curr, seconds):
        if date_curr is None:
            return False
        return date_curr + seconds