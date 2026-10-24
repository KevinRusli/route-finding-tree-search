"""Entry point.

Normal mode (stops at the first destination reached, as in the brief):
    python search.py <filename> <method>

Multi-destination mode (visits every destination, one leg at a time):
    python search.py <filename> <method> all          # every destination in the file
    python search.py <filename> <method> 4 5          # only these nodes

In multi mode the chosen method is run again and again: each leg starts at the
goal the previous leg reached and searches for the destinations still left.
The method itself decides which goal comes next, so the visiting order is the
method's own order, not necessarily the shortest overall tour.

Research method ALL (visits every destination in the cheapest order):
    python search.py <filename> ALL
"""
import sys
from problem import Problem, parse_file
from algorithms import dfs, bfs, gbfs, astar, cus1, cus2, visit_all

METHODS = {
    "DFS": dfs.search, "BFS": bfs.search, "GBFS": gbfs.search,
    "AS": astar.search, "CUS1": cus1.search, "CUS2": cus2.search,
}
# Research extension, not one of the six required methods.
RESEARCH_METHODS = {"ALL": visit_all.search}
ALL_METHODS = {**METHODS, **RESEARCH_METHODS}

USAGE = ("Usage: python search.py <filename> <method>\n"
         "       python search.py <filename> <method> all\n"
         "       python search.py <filename> <method> <node> <node> ...\n"
         "       python search.py <filename> ALL")


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        return
    filename, method = sys.argv[1], sys.argv[2].upper()
    if method not in ALL_METHODS:
        print(f"Unknown method: {method}. Choose from {', '.join(ALL_METHODS)}")
        return

    problem = parse_file(filename)
    extra = sys.argv[3:]

    # ---- Normal mode: one search, stop at the first goal reached ----
    if not extra:
        goal, nodes_created, path = ALL_METHODS[method](problem)
        print(f"{filename} {method}")
        if goal is None:
            print(f"No goal is reachable; {nodes_created}")
        else:
            print(f"{goal} {nodes_created}")
            print(" ".join(str(n) for n in path))
        return

    if method in RESEARCH_METHODS:
        print(f"{method} already visits every destination; run it without extra arguments")
        return

    # ---- Multi mode: work out which destinations must be visited ----
    if len(extra) == 1 and extra[0].lower() == "all":
        targets = list(problem.destinations)
    else:
        targets = []
        for word in extra:
            if not word.isdigit() or int(word) not in problem.coords:
                print(f"'{word}' is not a node in {filename}")
                print(USAGE)
                return
            if int(word) not in targets:  # ignore repeats
                targets.append(int(word))

    print(f"{filename} {method} (visit all: {' '.join(str(t) for t in targets)})")

    current = problem.origin
    remaining = list(targets)
    full_path = [current]
    visited = []
    total_nodes = 0
    leg = 0

    while remaining:
        leg += 1
        # Same map, but start where we are now and only look for goals left.
        leg_problem = Problem(problem.coords, problem.graph, current, remaining)
        goal, nodes_created, path = METHODS[method](leg_problem)
        total_nodes += nodes_created

        if goal is None:
            print(f"Leg {leg}: no remaining goal is reachable from {current}; {nodes_created}")
            break

        print(f"Leg {leg}: {goal} {nodes_created}")
        print(" ".join(str(n) for n in path))
        full_path += path[1:]  # path[0] is the current node, already in full_path
        visited.append(goal)
        remaining.remove(goal)
        current = goal

    # ---- Summary of the whole trip ----
    print(f"Visited: {' '.join(str(n) for n in visited) or 'none'}")
    if remaining:
        print(f"Not reachable: {' '.join(str(n) for n in remaining)}")
    print(f"Total nodes created: {total_nodes}")
    print(f"Full path: {' '.join(str(n) for n in full_path)}")
    print(f"Total cost: {problem.path_cost(full_path)}")


if __name__ == "__main__":
    main()