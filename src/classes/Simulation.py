from .Path import Path
from .Map import Map
from .PathFinder import PathFinder
from .Visualizer import Visualizer

class Simulation:
    def __init__(self, width, height, pass_allow_diagonal=False):
        self.map = Map(width, height)
        self.path_finder = PathFinder(self.map, pass_allow_diagonal)
        self.path = None

    def setup(self, start, goal, obstacles):
        self.map.set_start(*start)
        self.map.set_goal(*goal)
        for obstacle in obstacles:
            self.map.set_obstacle(*obstacle)

    def run_pathfinding(self):
        # Reset pathfinding state before running a new path search
        self.path_finder.reset_pathfinding_state()  # Ensures all nodes are reset

        start_node = self.map.get_node(*self.map.start)
        goal_node = self.map.get_node(*self.map.goal)
        self.path = self.path_finder.a_star_search(start_node, goal_node)

        if self.path.nodes:
            print("Path found with nodes:", self.path.get_path())
        else:
            print("No path found.")

    def reset_pathfinding(self):
        self.path_finder.reset_pathfinding_state()
        for row in self.map.nodes:
            for node in row:
                node.block = False  # Clears any obstacles

    def visualize(self):
        visualizer = Visualizer(self.map, self.path, self, cell_size=10)
        visualizer.run()

    def run(self):
        self.run_pathfinding()
        self.visualize()
