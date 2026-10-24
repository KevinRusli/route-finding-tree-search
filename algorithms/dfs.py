"""Depth-first search (DFS), uninformed.

Frontier's a stack, so last node in is the first one out. Since
neighbors() hands back kids in ascending order and we push them in
that same order, popping off the end still gets us the smallest
one first push goes low to high, pop flips it back. See
reversed() below for how that's done.

Contract: README.md and AGENTS.md.
"""


def search(problem):
    """Return (goal, nodes_created, path). goal is None if no goal is reachable."""
    origin = problem.origin
    nodes_created = 1  # the origin counts as 1

# Each stack entry is just the path so far (origin to here).
# We're using the path itself instead of a separate visited set
 # that way we can do the only loop check this assignment allows
# don't add a node that's already sitting on the current path.
    stack = [[origin]]

    while stack:
        path = stack.pop()
        node = path[-1]

        if problem.is_goal(node):
            return node, nodes_created, path

# Push the kids in reverse order stack's LIFO, so that flips
# it back and pops them smallest-first.
        for neighbor, _cost in reversed(problem.neighbors(node)):
            if neighbor in path:
                continue  # avoid cycling back onto the current path
            nodes_created += 1
            stack.append(path + [neighbor])

    return None, nodes_created, []
