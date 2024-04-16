import heapq
from .Path import Path

class PathFinder:
    def __init__(self, map):
        self.map = map

    def heuristic(self, a, b):
        return max(abs(a.x - b.x), abs(a.y - b.y))  # Chebyshev distance

    def a_star_search(self, start, goal, allow_diagonal=False):
        open_set = []
        heapq.heappush(open_set, (0, start))  # Push initial node with f=0
        start.g = 0
        start.h = self.heuristic(start, goal)
        start.f = start.h
        start.in_open_set = True

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                return self.reconstruct_path(current)

            current.in_closed_set = True
            for neighbor in self.get_neighbors(current, allow_diagonal):
                if neighbor.block or neighbor.in_closed_set:
                    continue

                diagonal = abs(neighbor.x - current.x) == 1 and abs(neighbor.y - current.y) == 1
                cost = 1.414 if diagonal and allow_diagonal else 1
                tentative_g_score = current.g + cost
                
                if tentative_g_score < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g_score
                    neighbor.h = self.heuristic(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h
                    if not neighbor.in_open_set:
                        heapq.heappush(open_set, (neighbor.f, neighbor))
                        neighbor.in_open_set = True

        return Path()  # Return an empty Path object if no path is found

    def get_neighbors(self, node, allow_diagonal):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if allow_diagonal:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
        
        neighbors = []
        for dx, dy in directions:
            x, y = node.x + dx, node.y + dy
            if 0 <= x < self.map.width and 0 <= y < self.map.height:
                neighbors.append(self.map.get_node(x, y))
        return neighbors

    def reconstruct_path(self, current):
        path = Path()
        while current:
            path.add_node(current)
            current = current.parent
        path.nodes.reverse()
        return path
