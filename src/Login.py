from getpass import getpass
from time import clock_gettime, CLOCK_REALTIME

class Login():
    def __init__(self, user, pswd) -> None:
        self._dbSession = MariaDBHelper()
        self._username  = user
        self._password  = pswd
        self._loginTime = clock_gettime(CLOCK_REALTIME)
    
    def getUsername(self) -> str:
        return self._username
    
    def timeOut(self) -> None:
        del(self)

    def isTimedOut(self) -> None:
        if (clock_gettime(CLOCK_REALTIME) - self._loginTime) > (30*60):
            self.sessionTimedOut()
            
    

    
            
