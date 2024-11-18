from src.visualisation.visualiser import Visualizer
from src.algorithms.Astar import Astar
from src.algorithms.Dijkstra import Dijkstra
from src.algorithms.DFS import DFS
from src.algorithms.BFS import BFS
import numpy as np


def heuristic(a,b):
    """
    Function that is used as a heuristic for the Astar algorithm

    Args:
        a (Tuple): Coords of Point 1
        b (Tuple): Coords of Point 2

    Returns:
        Metric of Distance between points 1,2
    """


    ###### FIll OUT HERE ######
    #Example: Manhatttan Distance
    distance = abs(a[0]-b[0]) + abs(a[1]-b[1])

    return distance

""" 
List Algorithms:
A list of all alogrithms that can be selected
For the ones that need a heurustic it needs to be initialised with it

The algos return:

None, if there is no path

An optimal path list, 
and a dictionary that has the all the current squares as keys and their neighbors in a list as values

"""


list_algorithms = [
    Astar(heuristic=heuristic),
    Dijkstra(),
    BFS(),
    DFS(),
    ]

def main ():
    
    vis = Visualizer(algorithms= list_algorithms,gridshape=(40,40))

if __name__ == '__main__':
    main()

    
    

 