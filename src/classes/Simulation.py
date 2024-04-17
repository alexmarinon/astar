from .Path import Path
from .Map import Map
from .PathFinder import PathFinder
from .Visualizer import Visualizer

class Simulation: # manages the simulation state
    def __init__(self, width, height, pass_allow_diagonal=False):
        self.map = Map(width, height)
        self.path_finder = PathFinder(self.map, pass_allow_diagonal)
        self.path = None

    def setup(self, start, goal, obstacles): # set goal, start
        self.map.set_start(*start)
        self.map.set_goal(*goal)
        for obstacle in obstacles:
            self.map.set_obstacle(*obstacle)

    def run_pathfinding(self):
        # reset pathfinding state before running a new path search
        self.path_finder.reset_pathfinding_state()

        # set start/end
        start_node = self.map.get_node(*self.map.start)
        goal_node = self.map.get_node(*self.map.goal)
        self.path = self.path_finder.a_star_search(start_node, goal_node) # generate a path object

        # after pathfinding
        if self.path.nodes:
            print("Path found with nodes:", self.path.get_path())
        else:
            print("No path found.")

    def reset_pathfinding(self): # reset the state
        self.path_finder.reset_pathfinding_state() # reset pathfinder
        for row in self.map.nodes: # clear blocks
            for node in row:
                node.block = False  # clears obstacles

    def clear_obstacles(self): # added some functions last minute to make creating a maze more intuitive
        """ Clears all obstacles from the map. """ # just learnt block comments from chenitha 🙏
        for row in self.map.nodes:
            for node in row:
                node.block = False

    def reset_path(self):
        """ Resets the pathfinding-related attributes of each node. """
        for row in self.map.nodes:
            for node in row:
                node.reset()

    def visualize(self):
        visualizer = Visualizer(self.map, self.path, self, cell_size=10) # generates visualizer object/display from simulation values
        visualizer.run() # runs

    def run(self):
        self.run_pathfinding()
        self.visualize()
