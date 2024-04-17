import pygame
from .Path import Path

class Visualizer:
    """
    Creates a display in PyGame to visually represent the PathFinder's Path result and the Map.
    """
    def __init__(self, map, path, simulation, cell_size=20):
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
        pygame.display.set_caption("Visualization")
        self.font = pygame.font.Font(None, 30)

        self.grid_color = (220, 220, 220)  # grey
        self.tile_color = (255, 255, 255)  # White
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

        pygame.init() # starts up pygame

    def draw_grid(self):
        """
        Generates a grid of pygame drawn rectangles from the cell size and the position of the x,y value of the node
        """
        for x in range(self.map.width):
            for y in range(self.map.height):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1) # color set to base grid

    def draw_menu(self):
        """
        The draw_menu() function generates the display data for the sidebar for the run loop to actually render via the draw() func.
        """
        pygame.draw.rect(self.screen, self.menu_color, pygame.Rect(self.width, 0, self.menu_width, self.height))  # draw the menu background

        # draw buttons and text from tuple of button blit object and the title.
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
            # centre text in the button
            self.screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) / 2, rect.y + (rect.height - text_surface.get_height()) / 2)) # blit renders on top of other element

    def draw(self): # renders the whole thing
        """
        The draw function generates the display data for the run loop to actually render.
        """
        self.screen.fill(self.tile_color)
        self.draw_grid()
        self.draw_menu()

        for x in range(self.map.width): # all nodes in grid x,y
            for y in range(self.map.height):
                node = self.map.get_node(x, y) # gets node at coords
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size) # draws node

                if node.block:
                    pygame.draw.rect(self.screen, self.obstacle_color, rect) # set to blocked color
                elif (x, y) == self.map.start:
                    pygame.draw.rect(self.screen, self.start_color, rect) # set to green
                elif (x, y) == self.map.goal:
                    pygame.draw.rect(self.screen, self.goal_color, rect) # set to red if goal

        if self.path and isinstance(self.path, Path): # checks if path not empty
            for node in self.path.nodes: 
                rect = pygame.Rect(node.x * self.cell_size, node.y * self.cell_size, self.cell_size, self.cell_size) # blue for found path
                pygame.draw.rect(self.screen, self.path_color, rect) # draws

        pygame.display.update() # update/re-render the frame

    def handle_events(self):
        """
        PyGame runs on an event-based architecture. Each action (like quitting the program, or having the mouse button state change)
        broadcasts a subscribable event. The event 'queue' is checked every cycle in the run loop.
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
                        self.process_click(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.mouse_button_down = False
                    self.last_node_toggled = None
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_button_down:
                    self.process_click(pygame.mouse.get_pos())
        return True
    
    def process_click(self, pos):
        """
        Get the position of the cursor on click event determine location for Node manipulation.
        """
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        if 0 <= x < self.map.width and 0 <= y < self.map.height:
            node = self.map.get_node(x, y)
            if node != self.last_node_toggled:
                node.block = not node.block
                self.last_node_toggled = node


    def reset_pathfinding(self):
        """
        Resets the path-finder state of the inherited PathFinder singleton object.
        """
        self.simulation.path_finder.reset_pathfinding_state() # reset callback to connected pathfinder

    def run(self): # render loop
        """
        Generates a render-update loop to sync internal state with PyGame's display.
        Utilises the handle_events() func to determine if the PyGame window should stay open (to prevent crashes/overload).
        """
        running = True
        while running:
            if not self.handle_events():
                running = False # cancel runtime
            self.draw()
        pygame.quit()