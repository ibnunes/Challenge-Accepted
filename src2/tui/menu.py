from tui.cli import sc, crt
from ..utils.read import Read


class MenuItem(object):
    def __init__(self, descr, func, isexit=False):
        self._description = descr
        self._function    = func
        self._isexit      = isexit

    def getDescription(self):
        return self._description

    def setDescription(self, descr):
        self._description = descr

    def getFunction(self):
        return self._function

    def setFunction(self, func):
        self._function = func

    def isExit(self):
        return self._isexit


class Menu(object):
    def __init__(self, title, subtitle="", itemlist=[]):
        self._title    = title
        self._subtitle = subtitle
        self._items    = itemlist
        self._count    = len(itemlist)
        self._error    = ""
        self._warning  = ""
        self._success


    def clearStdErr(self):
        self._warning = ""
        self._error   = ""
        self._success = ""


    def setError(self, err):
        self._success, self._warning = "", ""
        self._error = err


    def setWarning(self, warn):
        self._success, self._error = "", ""
        self._warning = warn


    def setSuccess(self, succ):
        self._warning, self._error = "", ""
        self._success = succ


    def show(self):
        print(f"{sc.HEADER}{self._title}{sc.ENDC}")
        if self._subtitle != "":
            print(self._subtitle)
        for i in range(1, self._count + 1):
            print(f"{i:3} > {self._items[i].getDescription()}")


    def exec(self, prompt="Option: "):
        opt = 0
        while True:
            self.show()
            crt.newLine()
            if self._warning != "":
                crt.writeWarning(self._warning)
            
            try:
                opt = Read.asInt(prompt)
            except ValueError:
                self.setWarning("Option is not a number.")
                continue
            
            try:
                if self._items[opt].isExit():
                    break
                else:
                    self._items[opt].getFunction()()
                self.clearStdErr()
            except IndexError:
                self.setWarning("Option not in menu.")
                continue
            except Exception as ex:
                self.setError(f"FATAL: {ex.message}")
                continue

    # TODO: addMenuItem
    # TODO: removeMenuItem

    # TODO peregrino: renderer


    @staticmethod
    def exec_menu(menu):
        menu.exec()

