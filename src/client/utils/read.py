from getpass import getpass
from tui.cli import crt

class Read(object):
    ERR_TYPE_MSG = "Type is not the expected one."
    
    @staticmethod
    def asInt(prompt=''):
        """
        Reads input and converts to int.

        Args:
            prompt (str, optional): Stdout prompt. Defaults to ''.

        Returns:
            int: Result from input casted into integer.
        """        
        return int(input(prompt))

    @staticmethod
    def tryAsInt(prompt=''):
        while True:
            try:
                return Read.asInt(prompt)
            except:
                crt.writeError(Read.ERR_TYPE_MSG)

    @staticmethod
    def asString(prompt=''):
        """
        Alias of input().

        Args:
            prompt (str, optional): Stdout prompt. Defaults to ''.

        Returns:
            str: Result from input. 
        """        
        return input(prompt)

    @staticmethod
    def asPassword(prompt=''):
        """
        Alias of getPass

        Args:
            prompt (str, optional): Stdout prompt. Defaults to ''.

        Returns:
            str: Result from hidden input.
        """        
        return getpass(prompt)
