from src.algorithms.base.algorithm import Algorithm
import numpy as np
from collections import deque

class BFS (Algorithm):

    def __init__(self,start=None,end=None,map=None):
        super().__init__("BFS")
        self.type = 'pathfinding'
        self.map = map
        self.start = start
        self.end = end

    def run_algorithm(self):
        queue = deque([self.start])
        visited = set([self.start])
        path = {self.start:None}
        pointsvisited = {}
        while queue:
            current_node = queue.popleft()
            pointsvisited[current_node] = []
            if current_node == self.end:
                return self.getPath(path),pointsvisited
            
            for neighbor in self.getNeighbors(current_node):
                pointsvisited[current_node].append(neighbor)

                if neighbor not in visited and not self.isWall(neighbor):
                    queue.append(neighbor)
                    visited.add(neighbor)
                    path[neighbor] = current_node

    def getNeighbors(self, node):
        x, y = node
        row,col = self.map.shape

        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < row and 0 <= ny < col]


    def getPath(self, path):
        current = self.end
        optimalpath = []
        while current != self.start:
            optimalpath.append(current)
            current = path[current]
        
        optimalpath.append(self.start)
        optimalpath.reverse()
        return optimalpath


    def isWall(self,node):
        if self.map[node] == -1:
            return True
        
    def __type__ (self):
        return self.type