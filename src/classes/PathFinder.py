from .Node import Node
from .Path import Path
import heapq

class PathFinder:
    def __init__(self, map, allow_diagonal=False):
        self.map = map
        self.allow_diagonal = allow_diagonal

    def heuristic(self, a, b, allow_diagonal):
        if allow_diagonal:
            return max(abs(a.x - b.x), abs(a.y - b.y))  # Chebyshev distance
        else:
            return abs(a.x - b.x) + abs(a.y - b.y)  # Manhattan distance

    def reset_pathfinding_state(self):
        for row in self.map.nodes:
            for node in row:
                node.g = float('inf')
                node.f = float('inf')
                node.h = 0
                node.parent = None
                node.in_open_set = False
                node.in_closed_set = False

    def a_star_search(self, start, goal):
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
            for neighbor in self.get_neighbors(current):
                if neighbor.block or neighbor.in_closed_set:
                    continue
                diagonal = abs(neighbor.x - current.x) == 1 and abs(neighbor.y - current.y) == 1
                cost = 1.414 if diagonal and self.allow_diagonal else 1
                tentative_g_score = current.g + cost
                if tentative_g_score < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g_score
                    neighbor.h = self.heuristic(neighbor, goal, self.allow_diagonal)
                    neighbor.f = neighbor.g + neighbor.h
                    if not neighbor.in_open_set:
                        heapq.heappush(open_set, (neighbor.f, neighbor))
                        neighbor.in_open_set = True
        return Path()

    def get_neighbors(self, node):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.allow_diagonal:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        neighbors = []
        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < self.map.width and 0 <= ny < self.map.height:
                next_node = self.map.get_node(nx, ny)
                if self.allow_diagonal and abs(dx) == 1 and abs(dy) == 1:
                    # Check for blocked corner-cutting
                    adjacent1 = self.map.get_node(node.x + dx, node.y)
                    adjacent2 = self.map.get_node(node.x, node.y + dy)
                    if not adjacent1.block and not adjacent2.block:
                        neighbors.append(next_node)
                elif not next_node.block:
                    neighbors.append(next_node)
        return neighbors

    def reconstruct_path(self, current):
        path = Path()
        while current:
            path.add_node(current)
            current = current.parent
        path.nodes.reverse()
        return path
