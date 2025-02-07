import pygame
import random
import time

class Enemy:
    def __init__(self, x, y, tile_size):
        self.tile_size = tile_size
        self.x = x * self.tile_size
        self.y = y * self.tile_size
        self.width = self.tile_size // 3.5
        self.height = self.tile_size // 3.5
        self.speed = 2
        self.health = 20
        self.damage = 5
        self.attack_range = 60 # Attack if within this distance
        self.detect_range = 200 # LoS start chasing player if player is within this range
        self.last_attack_time = 0
        self.attack_cooldown = 1 # 1 second between attacks

    def move_towards_player(self, player_x, player_y, dungeon_layout):
        # Moves toward the player if within LoS / detection range
        dx, dy = player_x - self.x, player_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5 # Euclidean distance

        if distance < self.detect_range: # Start chasing player
            if abs(dx) > abs(dy): # Move horizontally first
                new_x = self.x + self.speed * (1 if dx > 0 else -1)
                if self.can_move(new_x, self.y, dungeon_layout):
                    self.x = new_x
                else:
                    new_y = self.y + self.speed * (1 if dy > 0 else -1)
                    if self.can_move(self.x, new_y, dungeon_layout):
                        self.y = new_y
            else: # Move vertically first
                new_y = self.y + self.speed * (1 if dy > 0 else -1)
                if self.can_move(self.x, new_y, dungeon_layout):
                    self.y = new_y
                else:
                    new_x = self.x + self.speed * (1 if dx > 0 else -1)
                    if self.can_move(new_x, self.y, dungeon_layout):
                        self.x = new_x
        else: # Random movement if player is not in LoS
            if random.random() < 0.02: # Random movement chance
                new_x = self.x + self.speed * random.choice([-1, 1])
                new_y = self.y + self.speed * random.choice([-1, 1])
                if self.can_move(new_x, new_y, dungeon_layout):
                    self.x = new_x
                    self.y = new_y
    
    def can_move(self, new_x, new_y, dungeon_layout):
        """Checks if the new position is inside a walkable tile."""
        grid_x = int(new_x // self.tile_size)
        grid_y = int(new_y // self.tile_size)
        
        # FIX: Use separate indices instead of a tuple
        return dungeon_layout[grid_y][grid_x] == 0

    
    def attack(self, player):
        """Attacks player if in range and cooldown is over."""
        current_time = time.time()
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        if distance < self.attack_range and current_time - self.last_attack_time > self.attack_cooldown:
            player.health -= self.damage
            self.last_attack_time = current_time
            print(f"Enemy attacked! Player HP: {player.health}")

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))  # Red enemy