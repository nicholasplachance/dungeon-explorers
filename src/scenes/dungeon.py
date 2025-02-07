import pygame
import json
import random

from entities.player import Player
from entities.enemy import Enemy
from ui.hud import HUD
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Dungeon:
    def __init__(self, game_state, level=1):
        self.game_state = game_state
        self.font = pygame.font.Font(None, 36)
        self.tile_size = 80 # Matches JSON tile size
        self.load_random_dungeon(level)
        self.reset_dungeon(level)
        self.player = Player(self.player_start[0], self.player_start[1], self.tile_size)
        self.hud = HUD(self.player, self.dungeon_name) # Initialize HUD
        
        # Control difficulty scaling: More enemies on later levels
        enemy_count = min(3 + level * 2, 10)  # Max out at 10 enemies
        self.enemies = self.spawn_enemies(enemy_count)

    def load_random_dungeon(self, level):
        """Loads a random dungeon of the specified level."""
        with open("data/levels.json") as f:
            data = json.load(f)
            level_dungeons = [d for d in data["dungeons"] if d["level"] == level]

        if not level_dungeons:
            print(f"No dungeons found for level {level}!")
            return

        chosen_dungeon = random.choice(level_dungeons)  # ✅ Force new random choice
        print(f"Loading Dungeon: {chosen_dungeon['name']}")  # Debugging

        self.layout = chosen_dungeon["layout"]
        self.player_start = chosen_dungeon["player_start"]
        self.exit_position = chosen_dungeon["exit_position"]
        self.dungeon_name = chosen_dungeon["name"]

    def reset_dungeon(self, level):
        """Resets the dungeon to its default state, including enemies and player health."""
        self.player = Player(self.player_start[0], self.player_start[1], self.tile_size)
        self.player.health = 100  # Reset player health

        # Adjust enemy count based on level
        enemy_count = min(3 + level * 2, 10)
        self.enemies = self.spawn_enemies(enemy_count)
 
    def spawn_enemies(self, num_enemies):
        """Finds random valid tiles and spawns enemies."""
        spawn_locations = []
        rows, cols = len(self.layout), len(self.layout[0])
        player_start_x, player_start_y = self.player_start  # Player's starting grid position
        
        while len(spawn_locations) < num_enemies:
            rand_x, rand_y = random.randint(1, cols - 2), random.randint(1, rows - 2)

            # Ensure it's a walkable tile and not near the player
            if (
                self.layout[rand_y][rand_x] == 0  # Open space
                and (abs(rand_x - player_start_x) > 3 or abs(rand_y - player_start_y) > 3)  # Not too close to player
                and (rand_x, rand_y) not in spawn_locations  # Avoid duplicates
            ):
                spawn_locations.append((rand_x, rand_y))

        return [Enemy(x, y, self.tile_size) for x, y in spawn_locations]  # Create enemies at those positions

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
        for enemy in self.enemies[:]:  # Copy list to avoid issues with removal
            enemy.move_towards_player(self.player.x, self.player.y, self.layout)
            enemy.attack(self.player)

            if enemy.health <= 0:  # Remove dead enemies
                self.enemies.remove(enemy)

        # Check if player dies
        if self.player.health <= 0:
            self.game_state.dungeon = None
            self.game_state.change_state("DEATH")
            print("You Died!")  # TODO: Add a Game Over Screen


        # Check if player has reached the exit
        player_grid_x = self.player.x // self.tile_size
        player_grid_y = self.player.y // self.tile_size

        if (player_grid_x, player_grid_y) == tuple(self.exit_position):
            print("You Escaped!") # temporary log msg
            self.game_state.dungeon = None
            self.game_state.change_state("VICTORY") # Switch to victory screen
            # Reset player position
            self.player.x = self.player_start[0] * self.tile_size
            self.player.y = self.player_start[1] * self.tile_size

    def render(self, screen):
        # Calculate the dungeon's total width and height
        dungeon_width = len(self.layout[0]) * self.tile_size
        dungeon_height = len(self.layout) * self.tile_size

        # Get the camera position, ensuring it doesn't go off the dungeon
        cam_x, cam_y = self.player.get_camera_position(SCREEN_WIDTH, SCREEN_HEIGHT, dungeon_width, dungeon_height)

        # Render Dungeon Grid with Camera Offset
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size - cam_x
                y = row_index * self.tile_size - cam_y
                color = (155, 155, 155) if tile == 1 else (50, 50, 50)
                pygame.draw.rect(screen, color, (x, y, self.tile_size, self.tile_size))

        # Render Player and Enemies with Camera Offset
        player_x = self.player.x - cam_x
        player_y = self.player.y - cam_y
        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, self.player.width, self.player.height))

        for enemy in self.enemies:
            enemy.render(screen, cam_x, cam_y)  # ✅ Pass camera offsets to enemies

        # Render HUD last so it stays on screen
        self.hud.render(screen)
