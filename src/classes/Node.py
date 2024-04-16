class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.block = False  # Assuming a default value
        self.in_closed_set = False
        self.in_open_set = False

    def __lt__(self, other):  # ability to compare two nodes f values 
        return self.f < other.f
