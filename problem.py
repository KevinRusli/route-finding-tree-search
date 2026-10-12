"""Route Finding problem structure. Shared by every algorithm.

Owner: Kevin. Please tell him before changing anything in this file.
"""
import math


class Problem:
    def __init__(self, coords, graph, origin, destinations):
        self.coords = coords              # {node: (x, y)}
        self.graph = graph                # {node: [(neighbor, cost), ...]} (directed)
        self.origin = origin              # int
        self.destinations = destinations  # list of int

    def neighbors(self, n):
        """Neighbors of n as (neighbor, cost), sorted ascending by node number.

        Sorted order implements the assignment's tie-breaking rule.
        """
        return sorted(self.graph.get(n, []))

    def is_goal(self, n):
        return n in self.destinations

    def h(self, n):
        """Heuristic: Euclidean distance to the NEAREST destination."""
        x, y = self.coords[n]
        return min(
            math.hypot(x - self.coords[d][0], y - self.coords[d][1])
            for d in self.destinations
        )

    def edge_cost(self, a, b):
        """Cost of the directed edge a -> b, or None if that edge does not exist."""
        costs = [c for (nb, c) in self.graph.get(a, []) if nb == b]
        return min(costs) if costs else None

    def path_cost(self, path):
        """Total cost of a path (list of nodes), or None if any step is not a
        valid directed edge. A single-node path costs 0."""
        total = 0
        for a, b in zip(path, path[1:]):
            c = self.edge_cost(a, b)
            if c is None:
                return None
            total += c
        return total


def parse_file(filename):
    """Read a problem file and return a Problem.  TODO: Kevin

    Must cope with: blank lines, extra spaces, Windows line endings (\\r\\n),
    and node numbers that are not consecutive (see tests/test-19-messy-format.txt).
    """
    raise NotImplementedError("parse_file is not written yet")


def sample_problem():
    """Problem from the assignment sheet (tests/test-01-spec-example.txt), written
    by hand so teammates can test before parse_file exists."""
    coords = {1: (4, 1), 2: (2, 2), 3: (4, 4), 4: (6, 3), 5: (5, 6), 6: (7, 5)}
    edges = {
        (2, 1): 4, (3, 1): 5, (1, 3): 5, (2, 3): 4, (3, 2): 5, (4, 1): 6,
        (1, 4): 6, (4, 3): 5, (3, 5): 6, (5, 3): 6, (4, 5): 7, (5, 4): 8,
        (6, 3): 7, (3, 6): 7,
    }
    graph = {n: [] for n in coords}
    for (a, b), cost in edges.items():
        graph[a].append((b, cost))
    return Problem(coords, graph, 2, [5, 4])
