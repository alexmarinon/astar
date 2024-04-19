from .Node import Node
from .Path import Path
import heapq

class PathFinder:
    """
    Provides functionalities for pathfinding algorithms.
    """
    def __init__(self, map, allow_diagonal=False):
        """
        Initialise the pathfinder with a map and an option to allow diagonal movement (Chebyshev vs. Manhattan).

        :param map: The map object consisting of nodes.
        :param allow_diagonal: Boolean indicating if diagonal movement is allowed.
        """
        self.map = map  # map object containing nodes
        self.allow_diagonal = allow_diagonal  # toggles between Chebyshev and Manhattan distance

    def heuristic(self, a, b, allow_diagonal):
        """
        Calculate the heuristic distance between two nodes.

        :param a: The starting node.
        :param b: The goal node.
        :param allow_diagonal: Boolean indicating if diagonal movement is allowed.
        :return: Estimated distance as a float.
        """
        if allow_diagonal:
            return max(abs(a.x - b.x), abs(a.y - b.y))  # Chebyshev distance
        else:
            return abs(a.x - b.x) + abs(a.y - b.y)  # Manhattan distance

    def reset_pathfinding_state(self):
        """
        Reset the pathfinding state of each node in the map.
        """
        for row in self.map.nodes:
            for node in row:
                node.reset()

    def a_star_search(self, start, goal):
        """
        Perform the A* search algorithm to find the path from start to goal.
        More in-depth description is in the report document.

        :param start: The start node.
        :param goal: The goal node.
        :return: Path object from start to goal if a path exists.
        """
        open_set = []
        heapq.heappush(open_set, (0, start))
        start.g = 0
        start.h = self.heuristic(start, goal, self.allow_diagonal)
        start.f = start.h
        start.in_open_set = True

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                return self.reconstruct_path(current)
            current.in_closed_set = True
            for neighbour in self.get_neighbours(current):
                if neighbour.block or neighbour.in_closed_set:
                    continue
                diagonal = abs(neighbour.x - current.x) == 1 and abs(neighbour.y - current.y) == 1
                cost = 1.414 if diagonal and self.allow_diagonal else 1
                tentative_g_score = current.g + cost
                if tentative_g_score < neighbour.g:
                    neighbour.parent = current
                    neighbour.g = tentative_g_score
                    neighbour.h = self.heuristic(neighbour, goal, self.allow_diagonal)
                    neighbour.f = neighbour.g + neighbour.h
                    if not neighbour.in_open_set:
                        heapq.heappush(open_set, (neighbour.f, neighbour))
                        neighbour.in_open_set = True
        return Path()

    def get_neighbours(self, node):
        """
        Retrieve all possible neighbours of a node considering diagonal movement.

        :param node: The node for which neighbours are to be found.
        :return: A list of neighbouring nodes.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.allow_diagonal:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        neighbours = []
        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < self.map.width and 0 <= ny < self.map.height:
                next_node = self.map.get_node(nx, ny)
                if self.allow_diagonal and abs(dx) == 1 and abs(dy) == 1:
                    adjacent1 = self.map.get_node(node.x + dx, node.y)
                    adjacent2 = self.map.get_node(node.x, node.y + dy)
                    if not adjacent1.block and not adjacent2.block:
                        neighbours.append(next_node)
                elif not next_node.block:
                    neighbours.append(next_node)
        return neighbours

    def reconstruct_path(self, current):
        """
        Reconstruct the path from the goal node to the start node using parent references.

        :param current: The ending node of the path.
        :return: A path object tracing from start to goal.
        """
        path = Path()
        while current:
            path.add_node(current)
            current = current.parent
        path.nodes.reverse()
        return path
    
    def toggle_metric(self):
        """
        Toggle the metric used for calculating distances between allowing or disallowing diagonal movements.
        """
        self.allow_diagonal = not self.allow_diagonal
