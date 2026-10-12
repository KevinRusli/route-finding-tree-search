"""Entry point: python search.py <filename> <method>"""
import sys
from problem import parse_file
from algorithms import dfs, bfs, gbfs, astar, cus1, cus2

METHODS = {
    "DFS": dfs.search, "BFS": bfs.search, "GBFS": gbfs.search,
    "AS": astar.search, "CUS1": cus1.search, "CUS2": cus2.search,
}


def main():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        return
    filename, method = sys.argv[1], sys.argv[2].upper()
    if method not in METHODS:
        print(f"Unknown method: {method}. Choose from {', '.join(METHODS)}")
        return

    problem = parse_file(filename)
    goal, nodes_created, path = METHODS[method](problem)

    print(f"{filename} {method}")
    if goal is None:
        print(f"No goal is reachable; {nodes_created}")
    else:
        print(f"{goal} {nodes_created}")
        print(" ".join(str(n) for n in path))


if __name__ == "__main__":
    main()
