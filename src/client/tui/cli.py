import os

class crt(object):
    class color:
        """ Shell colors """
        if os.name == 'posix':
            HEADER    = '\033[95m'
            OKBLUE    = '\033[94m'
            OKCYAN    = '\033[96m'
            OKGREEN   = '\033[92m'
            WARNING   = '\033[93m'
            FAIL      = '\033[91m'
            DEBUG     = '\033[90m'
            ENDC      = '\033[0m'
            BOLD      = '\033[1m'
            UNDERLINE = '\033[4m'
        else:
            HEADER    = ''
            OKBLUE    = ''
            OKCYAN    = ''
            OKGREEN   = ''
            WARNING   = ''
            FAIL      = ''
            DEBUG     = ''
            ENDC      = ''
            BOLD      = ''
            UNDERLINE = ''

    @staticmethod
    def writeWarning(msg, end='\n'):
        """
        Writes a Warning.

        Args:
            msg (str): Message.
            end (str, optional): Ending to the message. Defaults to '\n'.
        """
        print(f"{crt.color.WARNING}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeError(msg, end='\n'):
        """
        Writes an Error.

        Args:
            msg (str): Message.
            end (str, optional): Ending to the message. Defaults to '\n'.
        """
        print(f"{crt.color.FAIL+crt.color.BOLD}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeFatal(msg, end='\n'):
        """
        Writes a Fatal Error.

        Args:
            msg (str): Message.
            end (str, optional): Ending to the message. Defaults to '\n'.
        """
        print(f"{crt.color.FAIL+crt.color.BOLD}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeInfo(msg, end='\n'):
        """
        Writes an Informative message.

        Args:
            msg (str): Message.
            end (str, optional): Ending to the message. Defaults to '\n'.
        """
        print(f"{crt.color.OKCYAN}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeSuccess(msg, end='\n'):
        """
        Writes a Success message.

        Args:
            msg (str): Message.
            end (str, optional): Ending to the message. Defaults to '\n'.
        """
        print(f"{crt.color.OKGREEN}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeDebug(msg, end='\n'):
        """
        Writes a Debug message.

        Args:
            msg (str): Message.
            end (str, optional): Ending to the message. Defaults to '\n'.
        """
        print(f"{crt.color.DEBUG}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeMessage(msg, end='\n'):
        """
        Writes a message.

        Args:
            msg (str): Message.
            end (str, optional): Ending to the message. Defaults to '\n'.
        """
        print(msg, end=end)

    @staticmethod
    def newLine():
        """Prints a new line"""        
        print(end='\n')

    @staticmethod
    def clearScreen():
        """Clears Screen on each OS"""        
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    @staticmethod
    def pause(msg="Press any key to continue... "):
        """
        Pauses the screen waiting for a key to be pressed.

        Args:
            msg (str, optional): Message. Defaults to "Press any key to continue... ".
        """        
        if os.name == 'nt':
            print(msg, end='')
            os.system("pause")
        else:
            os.system(f'read -s -n 1 -p "{msg}"')
