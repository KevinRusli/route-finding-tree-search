# Instructions for AI coding assistants

This repository is a university group assignment (COS30019, Route Finding with
tree-based search, Python). Several teammates each write ONE algorithm. The
contract below keeps everyone's code compatible. Follow it exactly, even if you
think another design is better. If something is unclear, ask the user instead of
guessing, and never change shared files on your own.

## Your scope

- Edit only the algorithm file the user owns (for example `algorithms/bfs.py`).
- Do NOT edit `problem.py`, `search.py`, `run_tests.py`, `tests/`, or another
  teammate's file. If you think one of them has a bug, tell the user and stop.
- Implement the algorithm from scratch with the standard library only
  (`heapq`, `collections`, `math` are fine). No search or graph libraries.

## The contract

```python
def search(problem):
    ...
    return goal, nodes_created, path
```

- `goal`: the destination node reached (int), or `None` if no goal is reachable.
- `nodes_created`: see counting rule below.
- `path`: list of nodes from the origin to the goal, e.g. `[2, 1, 4]`; `[]` on failure.
- Use only `problem.origin`, `problem.destinations`, `problem.neighbors(n)`
  (already sorted ascending, returns `(neighbor, cost)`), `problem.h(n)`,
  `problem.is_goal(n)`. Never read the input file yourself.
- No `print` inside algorithms. Only `search.py` prints.

## Rules that are easy to get wrong

1. **Tree-based search: no global visited/closed set.** The only loop check
   allowed is "do not add a node that is already on the current path".
2. **`nodes_created`**: the origin counts as 1, then +1 for every child node
   created and added to the frontier.
3. **Tie-breaking** (from the assignment): equal priority means the smaller node
   number is expanded first; if still equal, the node added to the frontier
   first. For heaps use tuples `(priority, node, counter, ...)` where `counter`
   increases on every push. Note the order: priority, then node, then counter.
4. **Goal test** happens when a node is removed from the frontier (expanded),
   not when it is generated.
5. A start that is already a destination returns `(origin, 1, [origin])`.
6. Multiple destinations are possible. Reaching ANY one of them is enough.
   `problem.h(n)` already uses the nearest destination.
7. Edges are directed. `problem.neighbors(n)` only returns edges leaving `n`.

## Before you say you are done

1. Run `python run_tests.py --methods <YOUR_METHOD>` and fix every FAIL/ERROR.
2. Run `python run_tests.py --methods <YOUR_METHOD> --cli` to check the output format.
3. Never edit `tests/expected.json` to make a test pass.
4. Do not claim the algorithm is optimal unless it guarantees it. If it does,
   tell the user to add the method name to `GUARANTEED_OPTIMAL` in `run_tests.py`.

## Code quality (marked, up to -10 for poor quality)

- A module docstring that names the algorithm and how it orders the frontier.
- Short comments on every non-obvious step.
- Clear names, small functions, no dead code.
- The user must be able to explain every line in the report and in class, so
  prefer simple code over clever code, and explain your choices when asked.

## AI use must be acknowledged

The assignment requires the report to state how AI was used. Remind the user to
add an entry to `docs/ai-usage-log.md` after every session that used AI.
