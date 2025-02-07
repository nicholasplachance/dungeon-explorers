import pygame
import time

class Player:
    def __init__(self, x, y, tile_size):
        self.tile_size = tile_size # 80px tiles
        self.x = x * self.tile_size
        self.y = y * self.tile_size
        self.width = self.tile_size // 3 # make the player half a tile
        self.height = self.tile_size // 3
        self.speed = 5 # movement speed
        self.health = 100
        self.attack_damage = 10
        self.attack_range = 60
        self.last_attack_time = 0
        self.attack_cooldown = 0.5  # Half a second between attacks

    def attack(self, enemies):
        """Attack any enemy within range."""
        current_time = time.time()
        if current_time - self.last_attack_time > self.attack_cooldown:
            for enemy in enemies:
                distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
                if distance < self.attack_range:
                    enemy.health -= self.attack_damage
                    print(f"Attacked enemy! Enemy HP: {enemy.health}")
                    if enemy.health <= 0:
                        enemies.remove(enemy)  # Remove dead enemy
                        print("Enemy defeated!")
                    self.last_attack_time = current_time
                    break  # Only hit one enemy per attack

    def can_move(self, new_x, new_y, dungeon_layout):
        """ Checks if all four corners of the player are in a walkable tile """
        grid_x1, grid_y1 = new_x // self.tile_size, new_y // self.tile_size  # Top-left
        grid_x2, grid_y2 = (new_x + self.width) // self.tile_size, new_y // self.tile_size  # Top-right
        grid_x3, grid_y3 = new_x // self.tile_size, (new_y + self.height) // self.tile_size  # Bottom-left
        grid_x4, grid_y4 = (new_x + self.width) // self.tile_size, (new_y + self.height) // self.tile_size  # Bottom-right

        # Check if all corners are inside walkable tiles (0)
        return (
            dungeon_layout[grid_y1][grid_x1] == 0 and
            dungeon_layout[grid_y2][grid_x2] == 0 and
            dungeon_layout[grid_y3][grid_x3] == 0 and
            dungeon_layout[grid_y4][grid_x4] == 0
        )

    def move(self, dx, dy, dungeon_layout):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        if self.can_move(new_x, self.y, dungeon_layout):
            self.x = new_x
        if self.can_move(self.x, new_y, dungeon_layout):
            self.y = new_y

    def get_camera_position(self, screen_width, screen_height, dungeon_width, dungeon_height):
        """Ensures the camera stays within the dungeon boundaries."""
        cam_x = max(0, min(self.x - screen_width // 2, dungeon_width - screen_width))
        cam_y = max(0, min(self.y - screen_height // 2, dungeon_height - screen_height))
        return cam_x, cam_y

    
    def render(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))