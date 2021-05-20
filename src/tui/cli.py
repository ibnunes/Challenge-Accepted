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
            ENDC      = ''
            BOLD      = ''
            UNDERLINE = ''

    @staticmethod
    def writeWarning(msg, end='\n'):
        print(f"{crt.color.WARNING}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeError(msg, end='\n'):
        print(f"{crt.color.FAIL+crt.color.BOLD}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeFatal(msg, end='\n'):
        print(f"{crt.color.FAIL+crt.color.BOLD}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeInfo(msg, end='\n'):
        print(f"{crt.color.OKCYAN}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeSuccess(msg, end='\n'):
        print(f"{crt.color.OKGREEN}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeDebug(msg, end='\n'):
        print(f"{crt.color.DEBUG}{msg}{crt.color.ENDC}", end=end)

    @staticmethod
    def writeMessage(msg, end='\n'):
        print(msg, end=end)

    @staticmethod
    def newLine():
        print(end='\n')

    @staticmethod
    def clearScreen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    @staticmethod
    def pause(msg="Press any key to continue... "):
        if os.name == 'nt':
            print(msg, end='')
            os.system("pause")
        else:
            os.system(f'read -s -n 1 -p "{msg}"')
