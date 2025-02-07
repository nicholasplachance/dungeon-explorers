import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from core.state import GameState

# Initialize pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# Game clock
clock = pygame.time.Clock()

# Game state manager
game_state = GameState()

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0)) # Clear Screen with Black

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and render the current game state
    game_state.update()
    game_state.render(screen)


    # Refresh display | refresh rate set by FPS
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()