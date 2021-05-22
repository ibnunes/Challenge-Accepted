from tui.cli import crt
from utils.read import Read
from copy import deepcopy as clone


class MenuItem(object):
    def __init__(self, descr, func, isexit=False):
        """
        Initializes a MenuItem.

        Args:
            descr (str): MenuItem description.
            func (function): Associated function.
            isexit (bool, optional): When true the option returns to previous Menu. Defaults to False.
        """        
        self._description = descr
        self._function    = func
        self._isexit      = isexit

    def getDescription(self):
        """
        Gets description.

        Returns:
            str: MenuItem description.
        """        
        return self._description

    def setDescription(self, descr):
        """
        Sets description.

        Args:
            descr (str): new MenuItem Description.
        """        
        self._description = descr

    def getFunction(self):
        """
        Gets MenuItem associated Function.

        Returns:
            function: function.
        """        
        return self._function

    def setFunction(self, func):
        """
        Sets new MenuItem function.

        Args:
            func (function): function.
        """        
        self._function = func

    def isExit(self):
        """
        Gets isexit.

        Returns:
            bool: isexit
        """        
        return self._isexit


class Menu(object):
    def __init__(self, title, subtitle="", itemlist=[]):
        """
        Initializes Menu.

        Args:
            title (str): Title
            subtitle (str, optional): Subtitle. Defaults to "".
            itemlist (list, optional): List of MenuItems. Defaults to [].
        """        
        self._title    = title
        self._subtitle = subtitle
        self._items    = itemlist
        self._count    = len(itemlist)
        self._error    = ""
        self._warning  = ""
        self._success  = ""


    def setTitle(self, title):
        """
        Sets Title of Menu.

        Args:
            title (str): New menu title.
        """
        self._title = title


    def withTitle(self, title):
        """
        Creates a copy of the menu with a different title.

        Args:
            title (str): Title

        Returns:
            Menu: Cloned Menu with a different title.
        """
        newme = clone(self)
        newme.setTitle(title)
        return newme


    def setSubtitle(self, subtitle):
        """
        Sets Subtitle of Menu.

        Args:
            subtitle (str): New menu Subtitle
        """
        self._subtitle = subtitle


    def clearStdErr(self):
        """Clears the Error/Warning/Success messages"""        
        self._warning = ""
        self._error   = ""
        self._success = ""


    def setError(self, err):
        """
        Sets an Error Message on Menu.

        Args:
            err (str): Error Message.
        """
        self._success, self._warning = "", ""
        self._error = err


    def setWarning(self, warn):
        """
        Sets a Warning Message on Menu.

        Args:
            err (str): Warning Message.
        """
        self._success, self._error = "", ""
        self._warning = warn


    def setSuccess(self, succ):
        """
        Sets a Success Message on Menu.

        Args:
            err (str): Success Message.
        """
        self._warning, self._error = "", ""
        self._success = succ


    def show(self):
        """Combines the Title, Subtitle and the MenuItems on a clear screen"""        
        crt.clearScreen()
        print(f"{crt.color.HEADER}{self._title}{crt.color.ENDC}")
        if self._subtitle != "":
            print(self._subtitle)
        for i in range(1, self._count + 1):
            print(f"{i:3} > {self._items[i-1].getDescription()}")


    def exec(self, prompt="Option: "):
        """
        Executes the Menu with a given Prompt.

        Args:
            prompt (str, optional): Stdout prompt. Defaults to "Option: ".

        Returns:
            int: Option selected.
        """        
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
        """
        Adds Item to Menu's itemList.

        Args:
            item (MenuItem): MenuItem
            at (int, optional): Specifies the index. Defaults to None.
        """        
        if at is None:
            self._items.append(item)
        else:
            self._items.insert(at, item)
        self._count = len(self._items)


    def removeItem(self, arg):
        """
        Removes Item from given MenuItem or index.

        Args:
            arg (any): Index of or the MenuItem wished to be removed from menu. 
        """        
        try:
            if type(arg) is MenuItem:
                self._items.remove(arg)
            else:
                del self._items[arg]
        finally:
            self._count = len(self._items)


    @staticmethod
    def exec_menu(menu):
        """
        Executes Menu.

        Args:
            menu (Menu): Menu to execute

        Returns:
            function: Execution function.
        """        
        return menu.exec

