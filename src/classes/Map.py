from .Node import Node

class Map:
    """
    Represents a grid of nodes, gives operations such as setting start and goal positions,
    adding obstacles, and accessing individual nodes.
    """

    def __init__(self, width, height):
        """
        Initialises the Map with specified dimensions and populate it with nodes.

        :param width: The number of nodes across (x-direction).
        :param height: The number of nodes down (y-direction).
        """
        self.width = width  # Number of nodes horizontally
        self.height = height  # Number of nodes vertically
        # Generate a 2D list of Node objects
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]
        self.start = None  # Starting node coordinates for pathfinding
        self.goal = None  # Goal node coordinates for pathfinding

    def set_obstacle(self, x, y):
        """
        Mark a node at the given coordinates as an obstacle.

        :param x: The x-coordinate of the node.
        :param y: The y-coordinate of the node.
        """
        self.nodes[x][y].block = True

    def set_goal(self, x, y):
        """
        Set the goal node for pathfinding.

        :param x: The x-coordinate of the goal node.
        :param y: The y-coordinate of the goal node.
        """
        self.goal = (x, y)

    def set_start(self, x, y):
        """
        Set the start node for pathfinding.

        :param x: The x-coordinate of the start node.
        :param y: The y-coordinate of the start node.
        """
        self.start = (x, y)

    def get_node(self, x, y):
        """
        Retrieve a node at specified coordinates.

        :param x: The x-coordinate of the node.
        :param y: The y-coordinate of the node.
        :return: The Node object at the specified coordinates.
        """
        return self.nodes[x][y]