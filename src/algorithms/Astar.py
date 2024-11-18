from src.algorithms.base.algorithm import Algorithm
import heapq 
import numpy as np

class Astar(Algorithm):
    def __init__(self,start,end,map:np.array,heuristic:callable):
        super().__init__("Astar")
        self.type = 'pathfinding'
        self.map = map
        self.start = start
        self.end = end
        self.heuristic = heuristic

    def run_algorithm(self):
        
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        
        row,col = self.map.shape


        #G Score: The cost of the path from the start node to n
        #F Score: The cost of the path from the start node to n through m
        g_score = np.full((row, col), np.inf)
        f_score = np.full((row, col), np.inf)

        g_score[self.start] = 0
        f_score[self.start] = self.heuristic(self.start, self.end)

        optimal_path = {}
        pointsvisited = {}
        while open_set:
            _, current =  heapq.heappop(open_set)
            #End Condition
            if current == self.end:
                return self.getPath(optimal_path, current), pointsvisited
            pointsvisited[current] = []
            for neighbor in self.getNeighbors(current):
                pointsvisited[current].append(neighbor)
                if self.isWall(neighbor):
                    continue

                t_gscore = g_score[current] + self.getCost(current, neighbor)
            
                if t_gscore < g_score[neighbor]:
                    optimal_path[neighbor] = current
                    g_score[neighbor] = t_gscore
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.end)
                    if neighbor not in [n[1] for n  in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None
    
    def getPath(self, optimal_path, current):
        path = []
        while current in optimal_path:
            path.append(current)
            current = optimal_path[current]

        path.append(self.start)
        return path[::-1]
    
    def getCost(self, current, neighbor):
        return self.map[neighbor]
    
    def getNeighbors(self, node):
        x, y = node
        row,col = self.map.shape

        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < row and 0 <= ny < col]

    def isWall(self,node):
        if self.map[node] == -1:
            return True

    def __type__ (self):
        return self.type

    def __heuristic__(self):
        return self.heuristic