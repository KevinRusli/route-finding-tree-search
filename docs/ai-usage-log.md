# AI usage log

The assignment requires the report to state how AI was used (or not used).
Each member adds a row after every session that involved an AI tool.
Be specific: what you asked, what you used, what you changed or rejected.

| Date | Member | Tool | What it was used for | What we kept / changed |
|---|---|---|---|---|
| 2026-10-12 | Kevin | Claude | Explained search concepts (UCS, IDA*, bidirectional search, g/h/f); wrote the project skeleton, README, AGENTS.md, 19 test cases, run_tests.py, the Problem class and parse_file | Kevin reviewed these before committing. CUS1 and the report are written by Kevin himself |
| 2026-10-16 | Ali Murtaza Shah Syed | Claude | Explained the search algorithms and the rest of the group's work (Problem class, parsing, tie-breaking and counting rules); gave code templates/structure for DFS and GBFS | Wrote and tested the DFS and GBFS code myself; ran `run_tests.py --methods DFS,GBFS --cli`, all tests passed |
| 2026-10-17 | Sakib Ahmed | Claude | Explained the CUS2 requirement ("informed method, least moves") and compared heuristic options (scaled Euclidean distance vs. a goal/non-goal estimate); wrote `algorithms/cus2.py` (A* where every edge counts as one move, h = 0 at a goal, otherwise 1) and ran `run_tests.py --methods CUS2 --cli`, all 19 tests passed |
