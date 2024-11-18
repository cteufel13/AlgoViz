from src.visualisation.visualiser import Visualiser
from src.algorithms.Astar import Astar
from src.algorithms.Dijkstra import Dijkstra
from src.algorithms.BFS import BFS
from src.algorithms.DFS import DFS
import numpy as np


def heuristic (a,b):
    #differnece
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

Astart = Astar(start=None,end=None,map=None,heuristic=heuristic)
Dijk = Dijkstra(start=None,end=None,map=None)
BFSt = BFS(start=None,end=None,map=None)
DFSt = DFS(start=None,end=None,map=None)
vis = Visualiser(algorithms= [Dijk,Astart,BFSt,DFSt],gridshape=(40,40))

 