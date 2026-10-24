# AI usage log

The assignment requires the report to state how AI was used (or not used).
Each member adds a row after every session that involved an AI tool.
Be specific: what you asked, what you used, what you changed or rejected.

| Date | Member | Tool | What it was used for | What we kept / changed |
|---|---|---|---|---|
| 2026-10-12 | Kevin Emmanuel Rusli | Claude | Explained search concepts (UCS, IDA*, bidirectional search, g/h/f); wrote the project skeleton, README, AGENTS.md, 19 test cases, run_tests.py, the Problem class and parse_file | Kevin reviewed these before committing. CUS1 and the report are written by Kevin himself |
| 2026-10-16 | Hassan Ali Shah SYED | Claude | Explained the assignment brief, repository structure, and key search concepts (nodes, edges, frontier, heuristic, and the 6 search methods), also explained how the multiple nodes work and how to implement in (`search.py`) | AI was used for concept explanations. Following team rules, Hassan tested BFS (`bfs.py`) and A* (`astar.py`) code manually, and the multiple nodes of (`search.py`) locally, and drafted README updates independently to be committed |
| 2026-10-16 | Ali Murtaza Shah Syed | Claude | Explained the search algorithms and the rest of the group's work (Problem class, parsing, tie-breaking and counting rules); gave code templates/structure for DFS and GBFS | Wrote and tested the DFS and GBFS code myself; ran `run_tests.py --methods DFS,GBFS --cli`, all tests passed |
| 2026-10-17 | Sakib Ahmed | Claude | Explained the CUS2 requirement ("informed method, least moves") and compared heuristic options (scaled Euclidean distance vs. a goal/non-goal estimate); wrote `algorithms/cus2.py` (A* where every edge counts as one move, h = 0 at a goal, otherwise 1) and ran `run_tests.py --methods CUS2 --cli`, all 19 tests passed | Reviewed every line of `cus2.py` and can explain it; chose the goal/non-goal heuristic because it is admissible for move counts; committed it as "CUS2: A* with unit step costs (fewest moves)" |

