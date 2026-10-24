"""Greedy best-first search (GBFS), informed.

Frontier's a priority queue, sorted purely by h(n) the
estimated straight-line distance to the nearest goal. We don't
care what it cost to get here, only how close it looks from
here. That's the "greedy" part, and what separates this from A*.

Contract: README.md and AGENTS.md."""
import heapq


def search(problem):
    """Return (goal, nodes_created, path). goal is None if no goal is reachable."""
    origin = problem.origin
    nodes_created = 1  # the origin counts as 1


# Heap entries: (h(node), node, counter, path). If two nodes tie
# on h, lower node number wins. Still tied? Counter breaks it by
# insertion order that's the tie-break rule the assignment wants.
    counter = 0
    frontier = [(problem.h(origin), origin, counter, [origin])]

    while frontier:
        _h, node, _c, path = heapq.heappop(frontier)

        if problem.is_goal(node):
            return node, nodes_created, path

        for neighbor, _cost in problem.neighbors(node):
            if neighbor in path:
                continue  # avoid cycling back onto the current path
            nodes_created += 1
            counter += 1
            heapq.heappush(frontier, (problem.h(neighbor), neighbor, counter, path + [neighbor]))

    return None, nodes_created, []
