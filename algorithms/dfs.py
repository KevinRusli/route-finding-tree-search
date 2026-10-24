"""Depth-first search (DFS), uninformed.

Frontier is a stack, so the last node in is the first one out.
neighbors() returns children in ascending order, so we push them in
reverse (largest first). That leaves the smallest child on top of the
stack, so it is expanded first (the assignment's tie-breaking rule).

Contract: README.md and AGENTS.md.
"""


def search(problem):
    """Return (goal, nodes_created, path). goal is None if no goal is reachable."""
    origin = problem.origin
    nodes_created = 1  # the origin counts as 1

    # Each stack entry is the path so far (origin to here). Keeping the
    # path instead of a visited set allows the only loop check this
    # assignment permits: don't add a node already on the current path.
    stack = [[origin]]

    while stack:
        path = stack.pop()
        node = path[-1]

        if problem.is_goal(node):
            return node, nodes_created, path

        # Push children in reverse order; the stack is LIFO, so they
        # come back out smallest first.
        for neighbor, _cost in reversed(problem.neighbors(node)):
            if neighbor in path:
                continue  # avoid cycling back onto the current path
            nodes_created += 1
            stack.append(path + [neighbor])

    return None, nodes_created, []