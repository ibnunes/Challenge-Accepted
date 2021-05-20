from getpass import getpass

class Read(object):
    ERR_TYPE_MSG = "Type is not the expected one."

    @staticmethod
    def asInt(prompt=''):
        return int(input(prompt))

    @staticmethod
    def asString(prompt=''):
        return input(prompt)

    @staticmethod
    def asPassword(prompt=''):
        return getpass(prompt)
