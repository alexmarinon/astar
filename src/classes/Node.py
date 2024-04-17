class Node:
    def __init__(self, x, y):
        """
        The Node is the fundamental building block of the path-finding system.
        """
        """
        A map is constructed of a grid of nodes
        A node can be blocked, transversible
        Has properties relating to the coordinates of the Node and the pathfinding cost
        """
        self.x = x # x val
        self.y = y # y val
        self.g = float('inf') # temporarily sets the score to infinite - cannot be transversed becaues the coordinates have not been rendered
        self.h = 0 # heuristic
        self.f = float('inf') # total cost
        self.parent = None # parent Node is used in PathFinding reconstructing to backtrack the pathfinding route
        self.block = False # If a Node is blocked, it is not transversible
        self.in_closed_set = False # if it has been examined
        self.in_open_set = False # if you cannot examine the Node

    def reset(self):
        self.g = float('inf')
        self.f = float('inf')
        self.h = 0
        self.parent = None
        self.in_closed_set = False
        self.in_open_set = False

    def __lt__(self, other):  # ability to compare two nodes f values. adds the ability to do comparison operators on Nodes
        return self.f < other.f # like Node1 < Node2
