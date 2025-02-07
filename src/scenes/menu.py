import pygame

class MainMenu:
    def __init__(self, game_state):
        self.game_state = game_state
        self.font = pygame.font.Font(None, 36)
        self.options = ["Start Game", "INFO", "Quit"]
        self.selected = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.selected = (self.selected + 1) % len(self.options)
        if keys[pygame.K_UP]:
            self.selected = (self.selected - 1) % len(self.options)
        if keys[pygame.K_RETURN]:
            if self.selected == 0:
                self.game_state.change_state("DUNGEON")
            elif self.selected == 1:
                self.game_state.change_state("INFO") # Open Info screen
            elif self.selected == 2:
                pygame.quit()
                exit()
    
    def render(self, screen):
        screen.fill((33,33, 33))
        for i, text in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (150, 150, 150)
            label = self.font.render(text, True, color)
            screen.blit(label, (300, 200 + i * 50))