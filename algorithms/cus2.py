"""CUS2: A* tree search for the fewest moves to any destination.

The frontier orders paths by moves taken + estimated moves remaining.
The estimate is 0 at a goal and 1 elsewhere, so it never overestimates.
Ties use the smaller node number, then the earlier insertion.

Edge costs are ignored. In search.py's "all" mode, each leg has the fewest
moves, but the combined trip is not guaranteed to have the fewest moves.
"""
import heapq


def search(problem):
    """Return (goal, nodes_created, path), or (None, nodes_created, []) on failure."""
    origin = problem.origin
    nodes_created = 1  # Count the origin.
    counter = 0

    # The origin has taken 0 moves, so its priority is just the estimate.
    estimate = 0 if problem.is_goal(origin) else 1
    # Each entry stores (priority, node, insertion order, path).
    frontier = [(estimate, origin, counter, [origin])]

    while frontier:
        # Remove the smallest entry; _ marks values we no longer need.
        _, node, _, path = heapq.heappop(frontier)

        # Accept a goal only when its path is removed from the frontier.
        if problem.is_goal(node):
            return node, nodes_created, path

        # Every outgoing edge counts as one move, regardless of its cost.
        for neighbor, _ in problem.neighbors(node):
            # Prevent loops on this path; allow the same node on other branches.
            if neighbor in path:
                continue

            new_path = path + [neighbor]  # Keep the original path unchanged.
            moves = len(new_path) - 1
            estimate = 0 if problem.is_goal(neighbor) else 1
            priority = moves + estimate  # A*: f = g + h.

            counter += 1
            heapq.heappush(frontier, (priority, neighbor, counter, new_path))
            nodes_created += 1  # Count each child added to the frontier.

    # No paths remain and no destination was reached.
    return None, nodes_created, []
