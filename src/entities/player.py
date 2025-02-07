import pygame


class Player:
    def __init__(self, x, y, tile_size):
        self.tile_size = tile_size # 80px tiles
        self.x = x * self.tile_size
        self.y = y * self.tile_size
        self.width = self.tile_size // 2 # make the player half a tile
        self.height = self.tile_size // 2
        self.speed = 5 # movement speed

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
    
    def render(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))