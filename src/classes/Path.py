# Path is basically just a list of nodes
class Path:
    def __init__(self, nodes=None):
        if nodes is None:
            nodes = []
        self.nodes = nodes

    def add_node(self, node):
        self.nodes.append(node)

    def get_path(self):
        return [(node.x, node.y) for node in self.nodes] # returns list of coordinates