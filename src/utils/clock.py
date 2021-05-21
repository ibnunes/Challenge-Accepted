import time

class Clock:
    @staticmethod
    def now():
        """
        Returns:
            float: current time
        """        
        return time.time()

    @staticmethod
    def isAfter(date_curr, date_next):
        """
        Compares times.

        Args:
            - date_curr (float)
            - date_next (float)

        Returns:
            bool: True if date_curr after date_next
        """        
        if date_curr is None or date_next is None:
            return False
        return date_curr > date_next

    @staticmethod
    def addSeconds(date_curr, seconds):
        """
        Returns the given time + given seconds.

        Args:
            date_curr (float): Given Dates
            seconds (int): Seconds

        Returns:
            float: date_curr[0] + seconds
        """        
        if date_curr is None:
            return False
        return date_curr[0] + seconds