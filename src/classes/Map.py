from .Node import Node

# A Map is kind of a datatype of a grid of Nodes.
class Map:
    def __init__(self, width, height): # create a map
        self.width = width # width (how many Nodes across)
        self.height = height # height
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)] # inline function to create array of arrays
        # allows to index the position of a Node with self.Nodes[0][0] - providing (0,0) coords of the node, top left
        self.start = None # start Node on the map, from which the pathfinding is calculated
        self.goal = None # end Node on the map, to which the pathfinding is calculated

    def set_obstacle(self, x, y): # sets a Node at the coordinates as an obstacle
        self.nodes[x][y].block = True 

    def set_goal(self, x, y): # sets node as the maps goal
        self.goal = (x, y)

    def set_start(self, x, y): # sets node as the maps start position
        self.start = (x, y)

    def get_node(self, x, y): # returns a Node object at the maps coordinates
        return self.nodes[x][y]
