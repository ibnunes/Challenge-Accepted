import os

# TODO: documentation


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Item():
    def __init__(self, descr, func) -> None:
        self._description = descr
        self._function = func

    def getDescription(self) -> str:
        return self._description

    def setDescription(self, descr) -> None:
        self._description = descr

    def getFunction(self):
        return self._function

    def setFunction(self, func) -> None:
        self._function = func


class Menu():
    def __init__(self, title, subtitle, itemlist) -> None:
        self._title = title
        self._subtitle = subtitle
        self._items = itemlist
        self._error = ""
        self._warning = ""
        self._success = ""

    def inputMenu(self) -> None:
        s = ""
        counter = 0

        for count, item in enumerate(self._items):
            description = item.getDescription()
            s += f"{bcolors.BOLD + str(count) + bcolors.ENDC}.{' '*3}{description}\n"
            counter += 1

        # print("\n" + "=:"*len(self._title) + "\n")
        
        Menu.clearScreen()
        index = input(
            f"{bcolors.HEADER + self._title + bcolors.ENDC}\n{self._subtitle}\n\n{s}\n{self._error+self._warning+self._success}\n >>> "
        )
        self._error, self._warning, self._success = "", "", ""
        
        try:
            (self._items[int(index)].getFunction())()
        except (IndexError, ValueError):
            self.addError("Wrong Input")
            self.inputMenu()

    def addError(self, err) -> None:
        self._success, self._warning = "", ""
        self._error = bcolors.FAIL + bcolors.BOLD + err + bcolors.ENDC
        
    def addWarning(self, warn) -> None:
        self._success, self._error = "", ""
        self._warning = bcolors.WARNING + warn + bcolors.ENDC
        
    def addSuccess(self, succ) -> None:
        self._warning, self._error = "", ""
        self._success = bcolors.OKGREEN + succ + bcolors.ENDC
        
    def clearScreen() -> None:
        if os.name == 'posix':
            # UNIX Systems
            _ = os.system('clear')
        else:
            # WINDOWS Systems
            _ = os.system('cls')


# Exemplo Caso tenham duvidas vejam isto...
if __name__ == "__main__":
    def f1():
        print("YEEEE")
        
    def f2():
        print("WOOOO")
        
    menu = Menu("Quilbanner todo pipi", "#bannerpipi", [Item("Clica-me, gostoso...", f1), Item("Não, clica EM mim... hmmmmm :3", f2)])
    menu.addError("FDS Tá td fdd")
    menu.addWarning("Ooolha bandeira amarela") # Só o ultimo definido funciona
    # menu.addSuccess("OH MARABILHAA")
    menu.inputMenu()
