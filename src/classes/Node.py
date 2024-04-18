class Node:
    """
    Represents a single node within a grid map for pathfinding purposes. Each node
    contains data related to its location, cost metrics for pathfinding, and its
    navigational properties.
    """

    def __init__(self, x, y):
        """
        Initialise a node with its position and default pathfinding values.

        :param x: The x-coordinate of the node in the grid.
        :param y: The y-coordinate of the node in the grid.
        """
        self.x = x  # x-coordinate
        self.y = y  # y-coordinate
        self.g = float('inf')  # Cost from start to node
        self.h = 0  # Heuristic cost from node to goal
        self.f = float('inf')  # Total cost (g + h)
        self.parent = None  # Parent node in the path
        self.block = False  # Whether the node is traversable
        self.in_closed_set = False  # Whether node has been processed
        self.in_open_set = False  # Whether node is in the queue to be processed

    def reset(self):
        """
        Reset the node's pathfinding metrics for a new pathfinding operation.
        """
        self.g = float('inf')
        self.f = float('inf')
        self.h = 0
        self.parent = None
        self.in_closed_set = False
        self.in_open_set = False

    def __lt__(self, other):
        """
        Define less-than for node comparison based on f cost. This supports
        comparisons between nodes, useful in priority queues during pathfinding.

        :param other: Another node to compare against.
        :return: True if this node's f cost is less than the other's.
        """
        return self.f < other.f