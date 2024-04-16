import heapq
from .Path import Path

class PathFinder:
    def __init__(self, map, allow_diagonal=False):
        self.map = map
        self.allow_diagonal = allow_diagonal

    def heuristic(self, a, b, allow_diagonal):
        if allow_diagonal:
            # Chebyshev distance (diagonal movement)
            return max(abs(a.x - b.x), abs(a.y - b.y))
        else:
            # Manhattan taxi-cab distance (no diagonal movement)
            return abs(a.x - b.x) + abs(a.y - b.y)

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

        return Path()  # Return an empty Path object if no path is found

    def get_neighbors(self, node):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.allow_diagonal:
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
