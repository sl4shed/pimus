class MenuManager:
    def __init__(self):
        self.menu_history = []

    def back(self, force=False):
        backable = self.menu_history[-1]["options"].get("backable", True)
        if force:
            backable = True
        if self.menu_history and backable:
            self.menu_history.pop()

    def add(self, menu, options={}):
        self.menu_history.append({"menu": menu, "options": options})

    def update(self):
        self.menu_history[-1]["menu"].update()
