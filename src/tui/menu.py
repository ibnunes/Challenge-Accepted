from tui.cli import crt
from utils.read import Read
from copy import deepcopy as clone


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
        self._success  = ""


    def setTitle(self, title):
        self._title = title


    def withTitle(self, title):
        newme = clone(self)
        newme.setTitle(title)
        return newme


    def setSubtitle(self, subtitle):
        self._subtitle = subtitle


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
        crt.clearScreen()
        print(f"{crt.color.HEADER}{self._title}{crt.color.ENDC}")
        if self._subtitle != "":
            print(self._subtitle)
        for i in range(1, self._count + 1):
            print(f"{i:3} > {self._items[i-1].getDescription()}")


    def exec(self, prompt="Option: "):
        opt = 0
        while True:
            self.show()
            crt.newLine()
            if self._warning != "":
                crt.writeWarning(self._warning)
            if self._error != "":
                crt.writeError(self._error)
            
            try:
                opt = Read.asInt(prompt) - 1
            except ValueError:
                self.setWarning("Option is not a number.")
                continue
            
            try:
                if self._items[opt].getFunction() is not None:
                    self._items[opt].getFunction()()
                if self._items[opt].isExit():
                    break
                self.clearStdErr()
            except IndexError:
                self.setWarning("Option not in menu.")
                continue
            except Exception as ex:
                self.setError(f"ERROR: {ex}")
                continue
        return opt + 1


    def addItem(self, item, at=None):
        if at is None:
            self._items.append(item)
        else:
            self._items.insert(at, item)


    def removeItem(self, arg):
        try:
            if type(arg) is MenuItem:
                self._items.remove(arg)
            else:
                del self._items[arg]
        finally:
            pass


    @staticmethod
    def exec_menu(menu):
        return menu.exec

