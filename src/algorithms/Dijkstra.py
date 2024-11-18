from src.algorithms.base.algorithm import Algorithm
import numpy as np
import heapq

class Dijkstra(Algorithm):

    def __init__(self,start=None,end=None,map=None):
        super().__init__("Dijkstra")
        self.type = 'pathfinding'
        self.map = map
        self.start = start
        self.end = end

    def run_algorithm(self):
        row,col = self.map.shape

        distances = np.full((row,col),np.inf)
        distances[self.start] = 0

        predecessor = np.full((row,col),None)

        priorityq = [(0,self.start)]
        pointsvisited = {}
    
        while priorityq:
            current_distance,current_cord =heapq.heappop(priorityq)
            pointsvisited[current_cord] = []
            if current_cord == self.end:
                return self.getPath(predecessor), pointsvisited
            
            if current_distance > distances[current_cord]:
                continue

            for neighbor in self.getNeighbors(current_cord):
                pointsvisited[current_cord].append(neighbor)
                distance = current_distance + self.map[neighbor]

                if self.isWall(neighbor):
                    continue

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessor[neighbor] = current_cord
                    heapq.heappush(priorityq,(distance,neighbor))



        shortest_distance = distances[self.end] if distances[self.end] < np.inf else None
         
        return self.getPath(predecessor)


    def getNeighbors(self, node):
        x, y = node
        row,col = self.map.shape

        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < row and 0 <= ny < col]
    
    def getPath(self, predecessor):
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = predecessor[current]
        path.append(self.start)
        return path[::-1]
    
    def isWall(self,node):
        if self.map[node] == -1:
            return True
        

    def __type__ (self):
        return self.type

    def __heuristic__(self):
        return self.heuristic