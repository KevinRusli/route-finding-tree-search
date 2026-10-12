"""Route Finding problem: the data every search algorithm works on.

Owner: Kevin. Please tell him before changing anything in this file.
"""
import math
import re


class Problem:
    def __init__(self, coords, graph, origin, destinations):
        self.coords = coords              # {node: (x, y)}
        # {node: [(neighbor, cost), ...]}, directed. Sorted once here so that
        # neighbors() always comes out in ascending node order (the tie-breaking rule).
        self.graph = {n: sorted(adj) for n, adj in graph.items()}
        self.origin = origin              # int
        self.destinations = destinations  # list of int

    def neighbors(self, n):
        """Edges leaving n as (neighbor, cost), ascending by neighbor. Do not modify."""
        return self.graph.get(n, [])

    def is_goal(self, n):
        return n in self.destinations

    def h(self, n):
        """Heuristic: straight-line distance from n to the NEAREST destination."""
        x, y = self.coords[n]
        return min(math.hypot(x - self.coords[d][0], y - self.coords[d][1])
                   for d in self.destinations)

    def edge_cost(self, a, b):
        """Cost of the directed edge a -> b, or None if there is no such edge."""
        costs = [c for nb, c in self.graph.get(a, []) if nb == b]
        return min(costs) if costs else None

    def path_cost(self, path):
        """Total cost of a path (list of nodes), or None if a step is not a valid
        directed edge. A path of one node costs 0."""
        total = 0
        for a, b in zip(path, path[1:]):
            cost = self.edge_cost(a, b)
            if cost is None:
                return None
            total += cost
        return total


_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
_SECTIONS = {"nodes:", "edges:", "origin:", "destinations:"}


def _numbers(text):
    """Every number in a line; an int unless it is written with a decimal point."""
    return [float(t) if "." in t else int(t) for t in _NUMBER.findall(text)]


def parse_file(filename):
    """Read a problem file and return a Problem.

    After each section keyword the lines look like this:
        Nodes:          1: (4,1)
        Edges:          (2,1): 4
        Origin:         2
        Destinations:   5; 4
    Blank lines, extra spaces and Windows line endings are ignored. Raises
    ValueError with the line number if a line cannot be read.
    """
    coords, edges = {}, []
    origin, destinations = None, []
    section = None

    with open(filename, encoding="utf-8-sig") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            if line.lower() in _SECTIONS:
                section = line.lower()
                continue

            nums = _numbers(line)
            if section == "nodes:" and len(nums) == 3:
                coords[int(nums[0])] = (nums[1], nums[2])
            elif section == "edges:" and len(nums) == 3:
                edges.append((int(nums[0]), int(nums[1]), nums[2]))
            elif section == "origin:" and len(nums) == 1:
                origin = int(nums[0])
            elif section == "destinations:" and nums:
                destinations.extend(int(n) for n in nums)
            else:
                raise ValueError(f"{filename}, line {lineno}: cannot read {line!r}")

    if origin is None:
        raise ValueError(f"{filename}: no origin given")
    if not destinations:
        raise ValueError(f"{filename}: no destinations given")
    for node in [origin, *destinations]:
        if node not in coords:
            raise ValueError(f"{filename}: node {node} has no coordinates")

    graph = {n: [] for n in coords}
    for a, b, cost in edges:
        if a not in coords or b not in coords:
            raise ValueError(f"{filename}: edge ({a},{b}) uses an unknown node")
        graph[a].append((b, cost))
    return Problem(coords, graph, origin, destinations)


def sample_problem():
    """The problem from the assignment sheet (tests/test-01-spec-example.txt),
    written by hand for quick experiments without a file."""
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
