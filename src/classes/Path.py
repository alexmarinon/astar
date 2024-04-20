class Path:
    """
    Represents a path as a list of nodes within a grid.
    """

    def __init__(self, nodes=None):
        """
        Initialise a Path instance.

        :param nodes: A list of nodes to initialise the path.
        """
        self.nodes = nodes if nodes is not None else []

    def add_node(self, node):
        """
        Append a node to the path.

        :param node: The node to be added to the path.
        """
        self.nodes.append(node)

    def get_path(self):
        """
        Get the list of node coordinates that make up the path.

        :return: A list of tuples, each representing the (x, y) coordinates of a node.
        """
        return [(node.x, node.y) for node in self.nodes]