class Read(object):
    ERR_TYPE_MSG = "Type is not the expected one."

    @staticmethod
    def asInt(prompt=''):
        return int(input(prompt))