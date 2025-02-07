import pygame
import time

class DeathScreen:
    def __init__(self, game_state):
        self.game_state = game_state
        self.font = pygame.font.Font(None, 64)
        self.alpha = 0  # Fade effect
        self.start_time = None

    def update(self):
        if self.start_time is None:
            self.start_time = time.time()  # Start timer when screen appears

        elapsed_time = time.time() - self.start_time

        # Fade-in effect (0 to 255 opacity)
        if self.alpha < 255:
            self.alpha += 5

        # After 3 seconds, return to the main menu
        if elapsed_time > 3:
            self.game_state.change_state("MENU")  # Restart from main menu

    def render(self, screen):
        screen.fill((0, 0, 0))  # Black background

        # Create a fading effect
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(self.alpha)
        screen.blit(fade_surface, (0, 0))

        # Draw "You Died!" text
        text = self.font.render("You Died... Better luck next time..", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
