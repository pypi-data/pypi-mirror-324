import heapq
from collections import defaultdict

from npycomp.reductions import clique_to_sat, threesat_to_clique

PROBLEMS = ["SAT", "3SAT", "clique"]

INDEX = {
    ("clique", "SAT"): clique_to_sat,
    ("3SAT", "clique"): threesat_to_clique,
}

_GRAPH = defaultdict(set)
for a, b in INDEX.keys():
    _GRAPH[a].add(b)


def path(start, end):
    """Find the shortest path between two nodes.

    Parameters
    ----------
    start : str
        The starting node.
    end : str
        The ending node.

    Returns
    -------
    list
        The shortest path between the two nodes.
    """
    paths = defaultdict(list)
    q = []
    heapq.heappush(q, (0, start))
    visited = set(start)
    while q:
        priority, current = heapq.heappop(q)

        for neighbour in _GRAPH[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                paths[neighbour].extend(paths[current] + [neighbour])
                heapq.heappush(q, (priority + 1, neighbour))

    return paths[end]
