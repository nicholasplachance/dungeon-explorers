from scenes.menu import MainMenu
from scenes.dungeon import Dungeon

class GamesState:
    def __init__(self):
        self.state = "MENU" # Start in the menu
        self.menu = MainMenu(self)
        self.dungeon = Dungeon(self)

    def update(self):
        if self.state == "MENU":
            self.menu.update()
        elif self.state == "DUNGEON":
            self.dungeon.update()

    def render(self, screen):
        if self.state == "MENU":
            self.menu.render(screen)
        elif self.state == "DUNGEON":
            self.dungeon.render(screen)
    
    def change_state(self, new_state):
        self.state = new_state
