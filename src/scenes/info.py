import pygame

class InfoScreen:
    def __init__(self, game_state, previous_state):
        self.game_state = game_state
        self.previous_state = previous_state # Store the scene to return to
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: # Return to previous screen when Esc is pressed
            self.game_state.change_state(self.previous_state)

    def render(self, screen):
        screen.fill((30, 30, 30))

        # Title
        title = self.title_font.render("Game Objective & Controls", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Instructions
        instructions = [
            "Objective: Reach the exit to escape the dungeon.",
            "Controls:",
            "- W/A/S/D: Move Up/Left/Down/Right",
            "- Press 'm': Return to Menu",
            "- I: Open Info Screen (In Dungeon)",
        ]

        y_offset = 150

        for line in instructions:
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (100, y_offset))
            y_offset += 40