import pandas as pd
from collections import defaultdict
import heapq


def dijkstra(graph, start, end):
    heap = [(0, start, [])]
    visited = set()
    while heap:
        (cost, vertex, path) = heapq.heappop(heap)
        if vertex not in visited:
            visited.add(vertex)
            path = path + [vertex]
            if vertex == end:
                return cost, path
            for neighbor, neighbor_cost in graph[vertex].items():
                heapq.heappush(heap, (cost + neighbor_cost, neighbor, path))
    return None, None


def find_route(start, end):
    df = pd.read_csv('Zeszyt1.csv', delimiter=';')
    graph = defaultdict(dict)
    for _, row in df.iterrows():
        graph[row['Rozpoczecie']][row['Zakonczenie']] = row['km']
        graph[row['Zakonczenie']][row['Rozpoczecie']] = row['km']
    return dijkstra(graph, start, end)