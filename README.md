# Route Finding: Tree-Based Search (COS30019 A2A)

Python implementation of tree-based search algorithms for the Route Finding
problem. The agent finds a path from an origin node to one of several
destination nodes on a 2D graph with directed, weighted edges.

Implemented methods: **DFS, BFS, GBFS, AS (A\*), CUS1, CUS2**.

## Usage

```
python search.py <filename> <method>
```

Methods: `DFS`, `BFS`, `GBFS`, `AS`, `CUS1`, `CUS2`

Example:

```
python search.py PathFinder-test-1.txt BFS
```

## Project Structure

```
search.py          # CLI entry point, dispatches to the chosen algorithm
problem.py         # Problem class, file parser, heuristic (shared by all)
algorithms/
  dfs.py  bfs.py  gbfs.py  astar.py  cus1.py  cus2.py
tests/             # test case files (aim for 15+)
```

One algorithm = one file. Please do not edit another member's file without
telling them first.

## Team Contract (everyone must follow)

### Function signature

Every file in `algorithms/` exposes exactly one function:

```python
def search(problem):
    ...
    return goal, nodes_created, path
```

- `goal`: the destination node reached (int), or `None` if no solution
- `nodes_created`: number of nodes created (see counting rule below)
- `path`: list of nodes from origin to goal, e.g. `[2, 3, 5]`; `[]` on failure

### The `problem` object

| Member | Description |
|---|---|
| `problem.origin` | Origin node (int) |
| `problem.destinations` | List of destination nodes |
| `problem.neighbors(n)` | List of `(neighbor, cost)`, already sorted ascending |
| `problem.h(n)` | Heuristic: Euclidean distance to the nearest destination |
| `problem.is_goal(n)` | `True` if `n` is a destination |

### Shared rules

1. **Tree-based search, no global visited set.** However, do not add a node
   that already appears on the *current path*. This prevents infinite loops
   on bidirectional edges.
2. **Counting `nodes_created`:** the origin counts as 1, then +1 for every
   child node created and added to the frontier.
3. **Tie-breaking (from the spec):** when priorities are equal, expand the
   smaller node number first; if still equal, expand the node that was added
   first (chronological order). For priority queues use tuples like
   `(priority, counter, ...)` where `counter` increases monotonically.
4. **Goal test:** performed when a node is *removed from the frontier*
   (expanded), not when it is generated.
5. **No `print` inside algorithms.** Only `search.py` prints output.

### Output format (printed by `search.py`)

```
<filename> <method>
<goal> <nodes_created>
<path: nodes separated by spaces>
```

Example:

```
PathFinder-test-1.txt BFS
4 12
2 1 4
```

If no goal is reachable: `<filename> <method>` followed by
`No goal is reachable; <nodes_created>`.

> Note: the exact counting rule and path format are pending confirmation
> from our tutor.

## Git Workflow

- Never commit directly to `main`.
- Create a branch per algorithm: `feature/dfs`, `feature/bfs`,
  `feature/gbfs`, `feature/astar`, `feature/cus1`, `feature/cus2`.
- Open a Pull Request when your algorithm works; at least one teammate
  reviews before merging.
- Write clear commit messages (e.g. `Add BFS with tie-breaking`).

Quick start:

```
git clone <repo-url>
git checkout -b feature/<your-algorithm>
# ...work, then...
git add .
git commit -m "Add <algorithm>"
git push -u origin feature/<your-algorithm>
```

## Task Assignment

| Task | Owner |
|---|---|
| Parser + `Problem` class | Kevin |
| CUS1, CUS2 | Kevin |
| DFS | TBD |
| BFS | TBD |
| GBFS | TBD |
| AS (A\*) | TBD |
| Test cases (15+) | TBD |
| Report | All |

## Deadline

Sunday, 25 Oct 2026, 11:59pm.
