from scenes.menu import MainMenu
from scenes.dungeon import Dungeon
from scenes.victory import VictoryScreen
from scenes.info import InfoScreen

class GamesState:
    def __init__(self):
        self.state = "MENU" # Start in the menu
        self.menu = MainMenu(self)
        self.dungeon = Dungeon(self)
        self.victory = VictoryScreen(self)
        self.info = None  # Info scene will be created dynamically

    def update(self):
        if self.state == "MENU":
            self.menu.update()
        elif self.state == "DUNGEON":
            self.dungeon.update()
        elif self.state == "VICTORY":
            self.victory.update()
        elif self.state == "INFO":
            self.info.update()

    def render(self, screen):
        if self.state == "MENU":
            self.menu.render(screen)
        elif self.state == "DUNGEON":
            self.dungeon.render(screen)
        elif self.state == "VICTORY":
            self.victory.render(screen)
        elif self.state == "INFO":
            self.info.render(screen)
    
    def change_state(self, new_state):
        # If switching to Info, store the previous state
        if new_state == "INFO":
            self.previous_state = self.state
            self.info = InfoScreen(self, self.previous_state)
        self.state = new_state
