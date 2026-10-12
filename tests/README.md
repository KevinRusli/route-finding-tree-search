# Test cases

Each `.txt` file follows the assignment format. `expected.json` stores, per file, whether a goal is
reachable and the minimum possible path cost (computed independently with Dijkstra).

| File | Scenario | Reachable | Optimal cost |
|---|---|---|---|
| `test-01-spec-example.txt` | Example from the assignment sheet (origin 2, goals 5 and 4) | yes | 10 |
| `test-02-origin-is-goal.txt` | Origin is also a destination: path is just the origin, cost 0 | yes | 0 |
| `test-03-no-path.txt` | Goal lies in a separate component, no solution exists | no | - |
| `test-04-one-way-trap.txt` | Straight-line route through node 2 is blocked by a one-way edge | yes | 10 |
| `test-05-single-edge.txt` | Smallest possible problem: one edge from origin to goal | yes | 5 |
| `test-06-equal-cost-goals.txt` | Two goals at the same cost from origin: tie-breaking decides | yes | 3 |
| `test-07-cycles.txt` | Bidirectional edges and a triangle: loops must be prevented | yes | 9 |
| `test-08-dead-ends.txt` | Several branches end in dead ends before the real route | yes | 13 |
| `test-09-long-chain.txt` | A straight chain of 10 nodes, only one route | yes | 18 |
| `test-10-diamond-equal-paths.txt` | Two different routes with identical cost: tie-breaking decides the path | yes | 10 |
| `test-11-greedy-trap.txt` | Closest-looking node leads to an expensive route: GBFS is not optimal here | yes | 14 |
| `test-12-tight-heuristic.txt` | Edge costs equal straight-line distance (Pythagorean triples) | yes | 22 |
| `test-13-many-goals.txt` | Five destination nodes at once | yes | 6 |
| `test-14-dense-complete.txt` | Complete directed graph on 7 nodes: many branches per node | yes | 15 |
| `test-15-fewer-hops-costs-more.txt` | Direct edge has fewest moves but is far more expensive than the long route | yes | 9 |
| `test-16-origin-no-outgoing.txt` | Origin only has incoming edges, so no goal is reachable | no | - |
| `test-17-grid-4x4.txt` | 4x4 grid with unit costs: huge number of equal-cost ties | yes | 6 |
| `test-18-random-20-nodes.txt` | Seeded random graph, 20 nodes, mixed one-way and two-way edges | yes | 36 |
| `test-19-messy-format.txt` | Parser stress test: Windows line endings, blank lines, trailing spaces, non-consecutive ids | yes | 9 |

## Adding a test

1. Create `tests/test-NN-short-name.txt` in the assignment format.
2. Add an entry to `expected.json` (scenario, reachable, optimal_cost).
3. Make sure every edge cost is at least the straight-line distance between its nodes, otherwise the Euclidean heuristic is not admissible.
