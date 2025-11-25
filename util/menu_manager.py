import inspect

from lib.services import Services


class MenuManager:
    def __init__(self):
        self.screen = Services.screen
        self.menu_history = []

    def back(self, force=False):
        backable = self.menu_history[-1]["options"].get("backable", True)
        if force:
            backable = True
        if self.menu_history and backable:
            self.menu_history.pop()
            self.screen.clear()
            self.menu_history[-1]["menu"].update()
            self.menu_history[-1]["menu"].draw()

    def add(self, menu, options={}):
        print("wtf")
        print(inspect.stack()[1][3])
        print(inspect.stack()[1][2])

        self.screen.clear()
        self.menu_history.append({"menu": menu, "options": options})
        self.menu_history[-1]["menu"].update()

    def update(self):
        self.menu_history[-1]["menu"].update()
