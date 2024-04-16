from .Map import Map
from .Node import Node
from .PathFinder import PathFinder
from .Path import Path
from .Visualizer import Visualizer

class Simulation:
    def __init__(self, width, height):
        self.map = Map(width, height)
        self.path_finder = PathFinder(self.map)
        self.path = None

    def setup(self, start, goal, obstacles):
        self.map.set_start(*start)
        self.map.set_goal(*goal)
        if obstacles:
            for obstacle in obstacles:
                self.map.set_obstacle(*obstacle)

    def run_pathfinding(self):
        start_node = self.map.get_node(*self.map.start)
        goal_node = self.map.get_node(*self.map.goal)
        self.path = self.path_finder.a_star_search(start_node, goal_node)
        if self.path.nodes:
            print("Path found with nodes:", self.path.get_path())
        else:
            print("No path found.")

    def visualize(self):
        visualizer = Visualizer(self.map, self.path, cell_size=10)
        visualizer.run()

    def run(self):
        self.run_pathfinding()
        self.visualize()
