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
        self.max_health = 20  # Store max health to calculate percentage
        self.damage = 5
        self.attack_range = 60  # Attack if within this distance
        self.detect_range = 200  # Start chasing player if close enough
        self.last_attack_time = 0
        self.attack_cooldown = 1  # 1 second between attacks
        self.font = pygame.font.Font(None, 20)  # Font for health text

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

    def render(self, screen, cam_x, cam_y):
        """Draws the enemy and their health bar with correct camera positioning."""
        enemy_x = self.x - cam_x
        enemy_y = self.y - cam_y

        # Draw enemy
        pygame.draw.rect(screen, (255, 0, 0), (enemy_x, enemy_y, self.width, self.height))

        # Draw health bar above the enemy
        self.draw_health_bar(screen, enemy_x, enemy_y)
    
    def draw_health_bar(self, screen, enemy_x, enemy_y):
        """Draws a health bar above the enemy."""
        bar_width = self.tile_size // 2
        bar_height = 6
        bar_x = enemy_x + (self.width // 2) - (bar_width // 2)
        bar_y = enemy_y - 10  # Position slightly above the enemy

        # Background Bar (Gray)
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Calculate health percentage
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)

        # Choose health bar color
        if health_percentage > 0.5:
            color = (0, 255, 0)  # Green
        elif health_percentage > 0.2:
            color = (255, 165, 0)  # Orange
        else:
            color = (255, 0, 0)  # Red

        # Health Bar (Dynamic)
        pygame.draw.rect(screen, color, (bar_x, bar_y, health_width, bar_height))

        # Draw HP text inside the bar
        # hp_text = f"{self.health}/{self.max_health}"
        # text_surface = self.font.render(hp_text, True, (255, 255, 255))
        # text_rect = text_surface.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        # screen.blit(text_surface, text_rect)