import pygame

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 28)  # Slightly smaller font for inside text
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.health_bar_x = 20
        self.health_bar_y = 20

    def render(self, screen):
        # Draw Health Bar Background (Gray Outline)
        pygame.draw.rect(screen, (50, 50, 50), (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height))

        # Calculate current health percentage
        health_percentage = self.player.health / 100
        health_width = int(self.health_bar_width * health_percentage)

        # Determine health bar color
        if health_percentage > 0.5:
            color = (0, 255, 0)  # Green
        elif health_percentage > 0.2:
            color = (255, 165, 0)  # Orange
        else:
            color = (255, 0, 0)  # Red

        # Draw actual health bar
        pygame.draw.rect(screen, color, (self.health_bar_x, self.health_bar_y, health_width, self.health_bar_height))

        # Create HP text (e.g., "60/100 HP")
        hp_text = f"{self.player.health}/100 HP"
        text_surface = self.font.render(hp_text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(
            self.health_bar_x + self.health_bar_width // 2,
            self.health_bar_y + self.health_bar_height // 2
        ))

        # Render the text inside the health bar
        screen.blit(text_surface, text_rect)

        # Draw Player Damage Text Below HP Bar
        damage_text = self.font.render(f"Damage: {self.player.attack_damage}", True, (255, 255, 255))
        screen.blit(damage_text, (self.health_bar_x, self.health_bar_y + 30))
