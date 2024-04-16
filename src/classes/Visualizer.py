import pygame
from .Path import Path

class Visualizer:
    def __init__(self, map, path, cell_size=20):
        self.map = map
        self.path = path
        self.cell_size = cell_size
        self.width = map.width * cell_size
        self.height = map.height * cell_size

        self.grid_color = (220, 220, 220) # grey
        self.tile_color = (255, 255, 255) # White
        self.obstacle_color = (50, 50, 50) # darker grey
        self.start_color = (0, 255, 0) # grreen
        self.goal_color = (255, 0, 0) # red
        self.path_color = (0, 0, 255) # blue

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Visualization")

    def draw_grid(self):
        for x in range(self.map.width):
            for y in range(self.map.height):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)

    def draw(self):
        self.screen.fill(self.tile_color)
        self.draw_grid()

        for x in range(self.map.width):
            for y in range(self.map.height):
                node = self.map.get_node(x, y)
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                
                if node.block:
                    pygame.draw.rect(self.screen, self.obstacle_color, rect)
                elif (x, y) == self.map.start:
                    pygame.draw.rect(self.screen, self.start_color, rect)
                elif (x, y) == self.map.goal:
                    pygame.draw.rect(self.screen, self.goal_color, rect)

        if self.path and isinstance(self.path, Path):
            for node in self.path.nodes:
                rect = pygame.Rect(node.x * self.cell_size, node.y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.path_color, rect)

        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
        pygame.quit()
