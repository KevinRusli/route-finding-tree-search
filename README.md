# Route Finding: Tree-Based Search (COS30019 A2A)

Python implementation of tree-based search algorithms for the Route Finding
problem. The agent finds a path from an origin node to one of several
destination nodes on a 2D graph with directed, weighted edges.

Implemented methods: **DFS, BFS, GBFS, AS (A\*), CUS1, CUS2**.

**Deadline: Sunday, 25 Oct 2026, 11:59pm.**

## Usage

```
python search.py <filename> <method>
```

Methods: `DFS`, `BFS`, `GBFS`, `AS`, `CUS1`, `CUS2`

Example:

```
python search.py tests/test-01-spec-example.txt BFS
```

## Project structure

```
search.py          # CLI entry point, dispatches to the chosen algorithm
problem.py         # Problem class, file parser, heuristic (shared by all)
run_tests.py       # runs methods on test files, validates, writes results.csv
algorithms/
  dfs.py  bfs.py  gbfs.py  astar.py  cus1.py  cus2.py
tests/             # 20 test files + expected.json + README.md (scenario list)
docs/ai-usage-log.md   # every member logs AI use here (needed for the report)
AGENTS.md          # rules for AI assistants (read automatically by most tools)
```

One algorithm = one file. Do not edit another member's file, `problem.py`,
`search.py`, `run_tests.py` or `tests/` without telling the owner first.

## Team contract (everyone must follow)

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
| `problem.path_cost(path)` | Total cost of a path, `None` if a step is not a valid edge |

### Shared rules

1. **Tree-based search, no global visited set.** However, do not add a node
   that already appears on the *current path*. This prevents infinite loops
   on bidirectional edges.
2. **Counting `nodes_created`:** the origin counts as 1, then +1 for every
   child node created and added to the frontier.
3. **Tie-breaking (from the spec):** when priorities are equal, expand the
   smaller node number first; if still equal, expand the node that was added
   first (chronological order). For priority queues use tuples
   `(priority, node, counter, ...)` where `counter` increases on every push.
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
tests/test-01-spec-example.txt BFS
4 10
2 1 4
```

If no goal is reachable: `<filename> <method>` followed by
`No goal is reachable; <nodes_created>`.

> Note: the exact counting rule and path format are pending confirmation
> from our tutor.

## Testing

`tests/` has 20 cases (the assignment asks for at least 15). Scenarios include
no solution, origin is a goal, one-way traps, cycles, dead ends, ties, many
goals, a dense graph, a 4x4 and a 10x10 grid, a seeded random graph, and a messy file format
for the parser. See `tests/README.md` for the full list.

```
python run_tests.py                       # every method on every test
python run_tests.py --methods BFS,DFS     # only your methods
python run_tests.py --files "tests/test-03*.txt"
python run_tests.py --cli                 # also checks the printed output format
```

For each result the runner checks that the path starts at the origin, ends at a
destination, uses only existing directed edges and never visits a node twice.
Methods in `GUARANTEED_OPTIMAL` (top of `run_tests.py`, currently `AS`) must also
match the optimal cost in `tests/expected.json`. A method that is still a stub
shows `TODO` and does not count as a failure. Every run writes `results.csv`
(goal, nodes created, cost, optimal or not, time), which is the raw data for the
Insights section of the report.

Rules for tests:

- Never edit `tests/expected.json` to make a test pass.
- When adding a test, also add its entry to `expected.json`, and make sure every
  edge cost is at least the straight-line distance between its two nodes
  (otherwise the Euclidean heuristic is not admissible).
- For a quick experiment without a file, `sample_problem()` in `problem.py`
  builds the assignment's example by hand.

## AI assistants

Most of us will use AI. `AGENTS.md` holds the rules that keep every AI-written
algorithm compatible, and most tools read it automatically (otherwise paste it
into your first message). The assignment requires the report to acknowledge AI
use, so add a row to `docs/ai-usage-log.md` after each session. You must be able
to explain every line you commit.

## Git workflow

- Work directly on `main`; there are no feature branches.
- Run `git pull` before every `git push` so you pick up teammates' changes.
- Only commit your own files (see "One algorithm = one file" above).
- Clear commit messages (e.g. `Add BFS with tie-breaking`).

```
git clone <repo-url>
# ...work, then...
git add algorithms/<your-file>.py
git commit -m "Add <algorithm>"
git pull
git push
```

If `git push` is rejected, someone pushed first: run `git pull`, then `git push` again.

## Task assignment

| Task | Owner |
|---|---|
| Parser + `Problem` class | Kevin |
| CUS1 | Kevin |
| Research | Kevin |
| CUS2 (informed method) | Sakib |
| DFS | Ali Murtaza Shah Syed |
| BFS | Hassan Ali Shah SYED |
| GBFS | Ali Murtaza Shah SYED |
| AS (A\*) | Hassan Ali Shah SYED |
| Report | All |
