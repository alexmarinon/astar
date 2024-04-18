import pygame
from .Path import Path

class Visualizer:
    """
    Creates a display using PyGame to visually represent the PathFinder's path result and the map layout.
    """

    def __init__(self, map, path, simulation, cell_size=20):
        """
        Initialise the visualiser with a map, path, simulation, and the size of each cell in the display.

        :param map: The map object containing nodes.
        :param path: Path object representing the current path.
        :param simulation: The simulation object handling the pathfinding.
        :param cell_size: The size of each cell in pixels.
        """
        pygame.init()

        self.simulation = simulation
        self.map = map
        self.path = path
        self.cell_size = cell_size
        self.width = map.width * cell_size
        self.height = map.height * cell_size

        self.mouse_button_down = False
        self.last_node_toggled = None

        self.menu_width = 200  # Increased menu width
        self.screen = pygame.display.set_mode((self.width + self.menu_width, self.height))
        pygame.display.set_caption("Visualisation")
        self.font = pygame.font.Font(None, 30)

        self.grid_color = (220, 220, 220)  # grey
        self.tile_color = (255, 255, 255)  # white
        self.obstacle_color = (50, 50, 50)  # darker grey
        self.start_color = (0, 255, 0)  # green
        self.goal_color = (255, 0, 0)  # red
        self.path_color = (0, 0, 255)  # blue
        self.menu_color = (100, 100, 100)  # medium grey
        self.button_color = (200, 200, 0)  # yellow

        button_width = 180
        button_height = 40
        button_margin_top = 50
        button_spacing = 50

        self.pathfind_button_rect = pygame.Rect(self.width + 10, button_margin_top, button_width, button_height)
        self.reset_button_rect = pygame.Rect(self.width + 10, button_margin_top + button_height + button_spacing, button_width, button_height)
        self.toggle_metric_button_rect = pygame.Rect(self.width + 10, button_margin_top + 2 * (button_height + button_spacing), button_width, button_height)
        self.clear_path_button_rect = pygame.Rect(self.width + 10, button_margin_top + 3 * (button_height + button_spacing), button_width, button_height)
        self.clear_obstacles_button_rect = pygame.Rect(self.width + 10, button_margin_top + 4 * (button_height + button_spacing), button_width, button_height)

    def draw_grid(self):
        """
        Generates a grid visualisation from cell sizes and node positions using PyGame's drawing functions.
        """
        for x in range(self.map.width):
            for y in range(self.map.height):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)  # Draw grid lines

    def draw_menu(self):
        """
        Draws the menu sidebar, including buttons for interaction with the simulation.
        """
        pygame.draw.rect(self.screen, self.menu_color, pygame.Rect(self.width, 0, self.menu_width, self.height))  # draw the menu background
        buttons = [
            (self.pathfind_button_rect, "Pathfind"),
            (self.reset_button_rect, "Reset"),
            (self.toggle_metric_button_rect, "Toggle Metric"),
            (self.clear_path_button_rect, "Clear Path"),
            (self.clear_obstacles_button_rect, "Clear Obstacles")
        ]
        for rect, text in buttons:
            pygame.draw.rect(self.screen, self.button_color, rect)
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) / 2, rect.y + (rect.height - text_surface.get_height()) / 2))

    def draw(self):
        """
        Renders the entire visualisation including map, path, and interactive menu.
        """
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
        """
        Processes PyGame events such as mouse clicks and button presses, updating the simulation state accordingly.
        Adds functionality to handle dragging to paint obstacles on the grid.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # Left mouse button
                    self.mouse_button_down = True
                    if self.pathfind_button_rect.collidepoint(pos):
                        self.simulation.run_pathfinding()
                        self.path = self.simulation.path
                    elif self.reset_button_rect.collidepoint(pos):
                        self.simulation.reset_pathfinding()
                        self.path = None
                    elif self.toggle_metric_button_rect.collidepoint(pos):
                        self.simulation.path_finder.toggle_metric()
                        self.simulation.run_pathfinding()
                        self.path = self.simulation.path
                    elif self.clear_path_button_rect.collidepoint(pos):
                        self.simulation.reset_path()
                        self.path = None
                    elif self.clear_obstacles_button_rect.collidepoint(pos):
                        self.simulation.clear_obstacles()
                    else:
                        # If the click is not on a button, process it as a grid click
                        self.process_click(pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.mouse_button_down = False
                    self.last_node_toggled = None  # Reset the last node toggled
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_button_down:
                    self.process_click(pygame.mouse.get_pos())
        return True

    def process_click(self, pos):
        """
        Processes mouse clicks on the grid, toggling the state of nodes between blocked and unblocked.
        """
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        if 0 <= x < self.map.width and 0 <= y < self.map.height:
            node = self.map.get_node(x, y)
            if node != self.last_node_toggled:
                node.block = not node.block
                self.last_node_toggled = node

    def reset_pathfinding(self):
        """
        Resets the internal state of the pathfinder to start a new pathfinding session.
        """
        self.simulation.path_finder.reset_pathfinding_state()

    def run(self):
        """
        Runs the main loop, handling rendering and events until the window is closed.
        """
        running = True
        while running:
            if not self.handle_events():
                running = False
            self.draw()
        pygame.quit()