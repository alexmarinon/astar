from .Node import Node
from .Path import Path
import heapq

class PathFinder: # pathfinder class contains the pathfinding logic
    def __init__(self, map, allow_diagonal=False):
        self.map = map # map
        self.allow_diagonal = allow_diagonal # toggle between chebyshev and manhattan distance

    def heuristic(self, a, b, allow_diagonal): # see Google Doc -> calculates transversible direct "distance"
        if allow_diagonal:
            return max(abs(a.x - b.x), abs(a.y - b.y))  # Chebyshev distance allows diagonal movement
        else:
            return abs(a.x - b.x) + abs(a.y - b.y)  # Manhattan distance does not allow diagonal movement

    def reset_pathfinding_state(self): # resets stored g,f,h values of each node
        for row in self.map.nodes:
            for node in row:
                node.reset()

    # a better explanation for the a star search is available on the Google Doc
    def a_star_search(self, start, goal):
        open_set = [] # all nodes that have not been investigated
        heapq.heappush(open_set, (0, start)) # heap queues are priority queues in Python. the 'priority' is the value of the 
        # nodes f val; essentially orders the list
        start.g = 0 # traversed distance cost
        start.h = self.heuristic(start, goal, self.allow_diagonal) # movement cost from start square to final destination, direct movement
        start.f = start.h # total cost of the start node. has no g val because there is no traversed distance
        start.in_open_set = True # start node is being examined therefore is in open set

        while open_set: # while open set is not empty (if empty then path found or no path available)
            current = heapq.heappop(open_set)[1] # smallest value of the open set
            if current == goal:
                return self.reconstruct_path(current) # if current node is the goal coords then its done and reconstruct the path
            current.in_closed_set = True # finished evaluating
            for neighbor in self.get_neighbors(current): # eval neighbors
                if neighbor.block or neighbor.in_closed_set:
                    continue # continue the loop but skip this node because its blocked or already examined
                diagonal = abs(neighbor.x - current.x) == 1 and abs(neighbor.y - current.y) == 1 # check if searched node is diagonal from current node
                cost = 1.414 if diagonal and self.allow_diagonal else 1 # cost is 1 (from length of node )except hypotenuse of diagonal (therefore traversed distance is root of 2)
                tentative_g_score = current.g + cost # temp g score, adds current g of Node and the transverse cost
                if tentative_g_score < neighbor.g: # if its cheaper to move with that Node 
                    neighbor.parent = current # set that nodes parent ot the current node, enables backtracking
                    neighbor.g = tentative_g_score # that found Nodes g score is the temp g score we created before
                    neighbor.h = self.heuristic(neighbor, goal, self.allow_diagonal) # h value of that node
                    neighbor.f = neighbor.g + neighbor.h # total cost of moving to that node
                    if not neighbor.in_open_set: # if that node is not currently in the open set
                        heapq.heappush(open_set, (neighbor.f, neighbor)) # add it to the open set with the f value as priority and neighbor as the object
                        neighbor.in_open_set = True
        return Path()

    def get_neighbors(self, node): # gets all neighbours of the node
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.allow_diagonal:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)]) # add these vals to the list

        neighbors = [] # found nodes[]
        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy # node x, y vals, adding direction vectors to find the coords
            if 0 <= nx < self.map.width and 0 <= ny < self.map.height: # node shouldnt go over map bounds
                next_node = self.map.get_node(nx, ny)
                if self.allow_diagonal and abs(dx) == 1 and abs(dy) == 1:
                    # check for blocked to stop corner cutting
                    adjacent1 = self.map.get_node(node.x + dx, node.y) # adjacent nodds
                    adjacent2 = self.map.get_node(node.x, node.y + dy) # adjacent nodes
                    if not adjacent1.block and not adjacent2.block:
                        neighbors.append(next_node) # adds to neighbors list if not blocked from transversing by a diagonal wall
                elif not next_node.block:
                    neighbors.append(next_node)
        return neighbors

    def reconstruct_path(self, current): # replay the path
        path = Path()
        while current: #current node (would be ending node if done pathfinding)
            path.add_node(current) #adds to path
            current = current.parent #current node is then parent node
        path.nodes.reverse() #flip to give start to end
        return path
    
    def toggle_metric(self):
        """ Toggle between allowing diagonal movement (Chebyshev) and not allowing it (Manhattan). """
        self.allow_diagonal = not self.allow_diagonal
