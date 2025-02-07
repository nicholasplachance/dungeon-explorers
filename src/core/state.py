from scenes.menu import MainMenu
from scenes.dungeon import Dungeon
from scenes.victory import VictoryScreen
from scenes.info import InfoScreen

class GameState:
    def __init__(self):
        self.state = "MENU"
        self.previous_state = None
        self.menu = MainMenu(self)
        self.dungeon = None  # We will create a new dungeon when starting a game
        self.victory = VictoryScreen(self)
        self.info = None  # Info screen will be created dynamically

    def update(self):
        if self.state == "MENU":
            self.menu.update()
        elif self.state == "DUNGEON":
            if self.dungeon is None:  # Create a fresh dungeon
                self.dungeon = Dungeon(self)
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
        if new_state == "DUNGEON":
            self.dungeon = Dungeon(self)  # Create a fresh dungeon on new game
        elif new_state == "INFO":
            self.previous_state = self.state
            self.info = InfoScreen(self, self.previous_state)

        self.state = new_state
