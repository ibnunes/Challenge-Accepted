import os

class sc:
    """ Shell colors """
    if os.name == 'posix':
        HEADER    = '\033[95m'
        OKBLUE    = '\033[94m'
        OKCYAN    = '\033[96m'
        OKGREEN   = '\033[92m'
        WARNING   = '\033[93m'
        FAIL      = '\033[91m'
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


class crt(object):
    @staticmethod
    def writeWarning(msg):
        print(f"{sc.WARNING}{msg}{sc.ENDC}")

    @staticmethod
    def writeError(msg):
        print(f"{sc.FAIL+sc.BOLD}{msg}{sc.ENDC}")

    @staticmethod
    def writeInfo(msg):
        print(f"{sc.OKCYAN}{msg}{sc.ENDC}")

    @staticmethod
    def writeSuccess(msg):
        print(f"{sc.OKGREEN}{msg}{sc.ENDC}")

    @staticmethod
    def writeMessage(msg):
        print(msg)

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
