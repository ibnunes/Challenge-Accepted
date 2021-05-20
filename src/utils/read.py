from getpass import getpass
from tui.cli import crt

class Read(object):
    ERR_TYPE_MSG = "Type is not the expected one."

    @staticmethod
    def asInt(prompt=''):
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
        return input(prompt)

    @staticmethod
    def asPassword(prompt=''):
        return getpass(prompt)
