from .Node import Node

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]
        self.start = None
        self.goal = None

    def set_obstacle(self, x, y):
        self.nodes[x][y].block = True

    def set_goal(self, x, y):
        self.goal = (x, y)

    def set_start(self, x, y):
        self.start = (x, y)

    def get_node(self, x, y):
        return self.nodes[x][y]
