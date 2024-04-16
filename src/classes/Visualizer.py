import pygame
from .Path import Path

class Visualizer:
    def __init__(self, map, path, simulation, cell_size=20):
        self.simulation = simulation

        self.map = map
        self.path = path
        self.cell_size = cell_size
        self.width = map.width * cell_size
        self.height = map.height * cell_size

        self.grid_color = (220, 220, 220)  # grey
        self.tile_color = (255, 255, 255)  # White
        self.obstacle_color = (50, 50, 50)  # darker grey
        self.start_color = (0, 255, 0)  # green
        self.goal_color = (255, 0, 0)  # red
        self.path_color = (0, 0, 255)  # blue
        self.menu_color = (100, 100, 100)  # medium grey
        self.button_color = (200, 200, 0)  # yellow

        pygame.init()
        self.screen = pygame.display.set_mode((self.width + 100, self.height))
        pygame.display.set_caption("Visualization")
        self.font = pygame.font.Font(None, 30)

    def draw_grid(self):
        for x in range(self.map.width):
            for y in range(self.map.height):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)

    

    def draw_menu(self):
        pygame.draw.rect(self.screen, self.menu_color, pygame.Rect(self.width, 0, 100, self.height))

        self.pathfind_button_rect = pygame.Rect(self.width + 10, 50, 80, 30)
        pygame.draw.rect(self.screen, self.button_color, self.pathfind_button_rect)
        pathfind_text = self.font.render('Pathfind', True, (0, 0, 0))
        self.screen.blit(pathfind_text, (self.width + 15, 55))

        self.reset_button_rect = pygame.Rect(self.width + 10, 100, 80, 30)
        pygame.draw.rect(self.screen, self.button_color, self.reset_button_rect)
        reset_text = self.font.render('Reset', True, (0, 0, 0))
        self.screen.blit(reset_text, (self.width + 25, 105))


    def draw(self):
        self.screen.fill(self.tile_color)
        self.draw_grid()
        self.draw_menu()

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    if self.pathfind_button_rect.collidepoint(pos):
                        self.simulation.run_pathfinding()
                        self.path = self.simulation.path
                    elif self.reset_button_rect.collidepoint(pos):
                        self.simulation.reset_pathfinding()
                        self.path = None  # Optionally clear the visual path
                    else:
                        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
                        if 0 <= x < self.map.width and 0 <= y < self.map.height:
                            node = self.map.get_node(x, y)
                            node.block = not node.block  # Toggle obstacle
        return True

    def reset_pathfinding(self):
        self.simulation.path_finder.reset_pathfinding_state()

    def run(self):
        running = True
        while running:
            if not self.handle_events():
                running = False
            self.draw()
        pygame.quit()
