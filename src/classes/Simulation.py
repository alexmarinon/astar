from .Path import Path
from .Map import Map
from .PathFinder import PathFinder
from .Visualizer import Visualizer

class Simulation:
    """
    Manages the simulation state, including setting up the map, running pathfinding,
    and visualisation via a PyGame interface.
    """

    def __init__(self, width, height, pass_allow_diagonal=False):
        """
        Initialise the simulation with the map size and the diagonal movement setting.

        :param width: Width of the map in nodes.
        :param height: Height of the map in nodes.
        :param pass_allow_diagonal: Boolean to allow diagonal movements in pathfinding.
        """
        self.map = Map(width, height)
        self.path_finder = PathFinder(self.map, pass_allow_diagonal)
        self.path = None

    def setup(self, start, goal, obstacles):
        """
        Set up the simulation map with start point, goal point, and obstacles.

        :param start: Tuple for the starting node coordinates.
        :param goal: Tuple for the goal node coordinates.
        :param obstacles: List of tuples for obstacle coordinates.
        """
        self.map.set_start(*start)
        self.map.set_goal(*goal)
        for obstacle in obstacles:
            self.map.set_obstacle(*obstacle)

    def run_pathfinding(self):
        """
        Execute the pathfinding algorithm using the A* search from the PathFinder.
        """
        self.path_finder.reset_pathfinding_state()
        start_node = self.map.get_node(*self.map.start)
        goal_node = self.map.get_node(*self.map.goal)
        self.path = self.path_finder.a_star_search(start_node, goal_node)

        if self.path.nodes:
            print("Path found with nodes:", self.path.get_path())
        else:
            print("No path found.")

    def reset_pathfinding(self):
        """
        Reset the pathfinding state and clear all obstacles from the map.
        """
        self.path_finder.reset_pathfinding_state()
        for row in self.map.nodes:
            for node in row:
                node.block = False

    def clear_obstacles(self):
        """
        Clear all obstacles from the map.
        """
        for row in self.map.nodes:
            for node in row:
                node.block = False

    def reset_path(self):
        """
        Reset the attributes of each node.
        """
        for row in self.map.nodes:
            for node in row:
                node.reset()

    def visualize(self):
        """
        Create and run the visualiser with the current simulation settings.
        """
        visualizer = Visualizer(self.map, self.path, self, cell_size=10)
        visualizer.run()

    def run(self):
        """
        Run the pathfinding and initiate the visualisation.
        """
        self.run_pathfinding()
        self.visualize()