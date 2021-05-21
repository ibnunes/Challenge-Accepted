from getpass import getpass
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
    

<<<<<<< HEAD:src/TUI.py
class Item(object):
=======

class Item():
>>>>>>> dev-ds:src/archive/TUI.py
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


class Menu(object):
    def __init__(self, title, subtitle, itemlist) -> None:
        self._title = title
        self._subtitle = subtitle
        self._items = itemlist
        self._error = ""
        self._warning = ""
        self._success = ""

    def show(self) -> None:
        s = ""
        for count, item in enumerate(self._items):
            description = item.getDescription()
            s += f"{bcolors.BOLD + str(count) + bcolors.ENDC}.{' '*3}{description}\n"
        
        Menu.clearScreen()
        index = input(
            f"{bcolors.HEADER + self._title + bcolors.ENDC}\n" + 
            f"{self._subtitle}\n\n" +
            f"{s}\n" +
            f"{self._error+self._warning+self._success}\n >>> "
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
            
            
class LoginScreen(object):
    def __init__(self):
        self._username = ""
        self._password = ""
        self._attempts = 3
        self._error    = ""
        self._warning  = ""
        self._success  = ""
        
    def show(self, loginFun):
        if not (self._attempts < 0):
            Menu.clearScreen()
            print(self._error + self._warning + self._success)
            try:
                self._username = input(bcolors.BOLD + "Username: " + bcolors.ENDC)
                self._password = getpass("Password: ")
                loginFun(self._username, self._password)
            except WrongPasswordOrUsername:
                self._attempts -= 1
                self.addWarning(f"Wrong username and/or password. {self._attempts} attempts left.")
                self._username, self._password = "", ""
                self.show()
            except NonValidatedPassword:
                self._attempts -= 1
                self.addError(f"You've inserted a Username and/or password with invalid characters.")
                self._username, self._password = "", ""
                self.show()
            
            return True
        
        else:
            return False
        
    def addError(self, err) -> None:
        self._success, self._warning = "", ""
        self._error = bcolors.FAIL + bcolors.BOLD + err + bcolors.ENDC

    def addWarning(self, warn) -> None:
        self._success, self._error = "", ""
        self._warning = bcolors.WARNING + warn + bcolors.ENDC

    def addSuccess(self, succ) -> None:
        self._warning, self._error = "", ""
        self._success = bcolors.OKGREEN + succ + bcolors.ENDC


# Exemplo Caso tenham duvidas vejam isto...
if __name__ == "__main__":
    def f1():
        print("YEEEE")
        
    def f2():
        print("WOOOO")
        
    menu = Menu(
        "Quilbanner todo pipi", 
        "#bannerpipi", 
        [Item("Clica-me, gostoso...", f1),
         Item("Não, clica EM mim... hmmmmm :3", f2)]
    )
    menu.addError("FDS Tá td fdd")
    menu.addWarning("Ooolha bandeira amarela") # Só o ultimo definido funciona
    # menu.addSuccess("OH MARABILHAA")
    menu.show()
