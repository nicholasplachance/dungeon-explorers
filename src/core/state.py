from scenes.menu import MainMenu
from scenes.dungeon import Dungeon
from scenes.victory import VictoryScreen

class GamesState:
    def __init__(self):
        self.state = "MENU" # Start in the menu
        self.menu = MainMenu(self)
        self.dungeon = Dungeon(self)
        self.victory = VictoryScreen(self)

    def update(self):
        if self.state == "MENU":
            self.menu.update()
        elif self.state == "DUNGEON":
            self.dungeon.update()
        elif self.state == "VICTORY":
            self.victory.update()

    def render(self, screen):
        if self.state == "MENU":
            self.menu.render(screen)
        elif self.state == "DUNGEON":
            self.dungeon.render(screen)
        elif self.state == "VICTORY":
            self.victory.render(screen)
    
    def change_state(self, new_state):
        self.state = new_state
