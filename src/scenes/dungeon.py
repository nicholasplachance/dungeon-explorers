import pygame


class Dungeon:
    def __init__(self, game_state):
        self.game_state = game_state
        self.font = pygame.font.Font(None, 36)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game_state.change_state("MENU") # Allow return to menu

    def render(self, screen):
        screen.fill((50, 50, 50))
        text = self.font.render("Dungeon Scene - Press ESC to return to menu", True, (255, 255, 255))
        screen.blit(text, (200, 200))