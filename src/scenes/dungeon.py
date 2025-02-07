import pygame
import json
from entities.player import Player
from entities.enemy import Enemy

class Dungeon:
    def __init__(self, game_state):
        self.game_state = game_state
        self.font = pygame.font.Font(None, 36)
        self.tile_size = 80 # Matches JSON tile size
        self.load_dungeon()
        self.player = Player(self.player_start[0], self.player_start[1], self.tile_size)
        self.enemies = [Enemy(5, 5, self.tile_size)]  # Spawn one enemy

    def load_dungeon(self):
        with open("data/levels.json") as f:
            data = json.load(f)
            self.layout = data["dungeons"][0]["layout"] # Load first dungeon
            self.player_start = data["dungeons"][0]["player_start"]
            self.exit_position = data["dungeons"][0]["exit_position"]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.player.move(0, -1, self.layout)  # Up
        if keys[pygame.K_s]: self.player.move(0, 1, self.layout)   # Down
        if keys[pygame.K_a]: self.player.move(-1, 0, self.layout)  # Left
        if keys[pygame.K_d]: self.player.move(1, 0, self.layout)   # Right

         # Open Info Screen
        if keys[pygame.K_i]:
            self.game_state.change_state("INFO")

        if keys[pygame.K_m]:
            self.game_state.change_state("MENU") # Allow return to menu

        if keys[pygame.K_SPACE]:  # Player attacks with spacebar
            self.player.attack(self.enemies)

        # Enemy logic
        for enemy in self.enemies:
            enemy.move_towards_player(self.player.x, self.player.y, self.layout)
            enemy.attack(self.player)

        # Check if player dies
        if self.player.health <= 0:
            print("You Died!")  # TODO: Add a Game Over Screen
            self.game_state.change_state("MENU")


        # Check if player has reached the exit
        player_grid_x = self.player.x // self.tile_size
        player_grid_y = self.player.y // self.tile_size

        if (player_grid_x, player_grid_y) == tuple(self.exit_position):
            print("You Escaped!") # temporary log msg
            self.game_state.change_state("VICTORY") # Switch to victory screen
            # Reset player position
            self.player.x = self.player_start[0] * self.tile_size
            self.player.y = self.player_start[1] * self.tile_size

    def render(self, screen):
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                color = (255, 255, 255) if tile == 1 else (50, 50, 50) # White walls, dark floors
                pygame.draw.rect(screen, color, (x, y , self.tile_size, self.tile_size))
        
        self.player.render(screen) # Draw player after rendering the dungeon
        for enemy in self.enemies:
            enemy.render(screen)