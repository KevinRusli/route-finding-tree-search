"""Run search methods on the test files, validate the results, save results.csv.

Usage:
    python run_tests.py                          # every method on every test
    python run_tests.py --methods BFS,DFS        # only some methods
    python run_tests.py --files "tests/test-03*.txt"
    python run_tests.py --cli                    # also check the printed output format
    python run_tests.py --methods ALL            # research: visit every destination

A result is PASS when the returned path is valid (starts at the origin, ends at
a destination, uses only existing directed edges, visits no node twice). Methods
listed in GUARANTEED_OPTIMAL must also match the optimal cost in expected.json.
Methods that are still a stub show TODO; they never count as a failure.
"""
import argparse
import csv
import glob
import json
import os
import re
import subprocess
import sys
import time

from problem import parse_file
from search import METHODS, ALL_METHODS

# Methods that must always return a minimum-cost path. Add yours here only if
# your algorithm really guarantees optimality (e.g. UCS, A* with the Euclidean h).
GUARANTEED_OPTIMAL = {"AS"}

TESTS_DIR = "tests"


def load_expected():
    with open(os.path.join(TESTS_DIR, "expected.json")) as f:
        return json.load(f)


def validate(problem, method, result, exp):
    """Return (status, note, cost) for one result."""
    try:
        goal, nodes_created, path = result
    except (TypeError, ValueError):
        return "FAIL", "search() must return (goal, nodes_created, path)", None

    if not isinstance(nodes_created, int):
        return "FAIL", "nodes_created must be an int", None

    if not exp["reachable"]:
        if goal is not None:
            return "FAIL", "returned a goal but none is reachable", None
        return "PASS", "", None

    if goal is None:
        return "FAIL", "returned no goal but one is reachable", None
    if goal not in problem.destinations:
        return "FAIL", f"goal {goal} is not a destination", None
    if not path or path[0] != problem.origin or path[-1] != goal:
        return "FAIL", "path must start at the origin and end at the goal", None
    if len(set(path)) != len(path):
        return "FAIL", "path visits a node twice", None
    cost = problem.path_cost(path)
    if cost is None:
        return "FAIL", "path uses a missing or wrong-direction edge", None
    if nodes_created < len(path):
        return "FAIL", "nodes_created is smaller than the path length", cost
    if method in GUARANTEED_OPTIMAL and abs(cost - exp["optimal_cost"]) > 1e-9:
        return "FAIL", f"cost {cost} but optimal is {exp['optimal_cost']}", cost
    return "PASS", "", cost


def validate_all(problem, result, exp):
    """Research method ALL: the path must reach EVERY destination at the cheapest
    total cost. Unlike the six main methods it may pass through a node twice."""
    try:
        goal, nodes_created, path = result
    except (TypeError, ValueError):
        return "FAIL", "search() must return (goal, nodes_created, path)", None
    if exp["visit_all_cost"] is None:
        if goal is None:
            return "PASS", "", None
        return "FAIL", "returned a goal but not every destination is reachable", None
    if goal is None:
        return "FAIL", "returned no goal but every destination is reachable", None
    if not path or path[0] != problem.origin or path[-1] != goal:
        return "FAIL", "path must start at the origin and end at the goal", None
    missing = [d for d in problem.destinations if d not in path]
    if missing:
        return "FAIL", f"path never visits destination(s) {missing}", None
    cost = problem.path_cost(path)
    if cost is None:
        return "FAIL", "path uses a missing or wrong-direction edge", None
    if abs(cost - exp["visit_all_cost"]) > 1e-9:
        return "FAIL", f"cost {cost} but cheapest is {exp['visit_all_cost']}", cost
    return "PASS", "", cost


def check_cli_format(filename, method):
    """Run search.py as a subprocess and check the three-line output format."""
    proc = subprocess.run([sys.executable, "search.py", filename, method],
                          capture_output=True, text=True)
    lines = proc.stdout.strip().splitlines()
    if proc.returncode != 0 or len(lines) < 2:
        return False, (proc.stderr.strip().splitlines() or ["no output"])[-1]
    if lines[0] != f"{filename} {method}":
        return False, f"first line should be '{filename} {method}'"
    if not (re.fullmatch(r"\d+ \d+", lines[1]) or lines[1].startswith("No goal")):
        return False, "second line should be '<goal> <nodes_created>'"
    return True, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--methods", default=",".join(METHODS))
    ap.add_argument("--files", default=os.path.join(TESTS_DIR, "test-*.txt"))
    ap.add_argument("--cli", action="store_true", help="also check search.py output format")
    args = ap.parse_args()

    methods = [m.strip().upper() for m in args.methods.split(",")]
    files = sorted(glob.glob(args.files))
    expected = load_expected()
    if not files:
        sys.exit("No test files matched.")

    rows, counts = [], {"PASS": 0, "FAIL": 0, "ERROR": 0, "TODO": 0}
    print(f"{'file':<34}{'method':<7}{'status':<7}{'goal':<6}{'nodes':<7}{'cost':<7}{'optimal':<9}{'ms':<8}note")
    for fn in files:
        base = os.path.basename(fn)
        exp = expected[base]
        problem = parse_file(fn)
        for m in methods:
            start = time.perf_counter()
            goal = nodes = cost = None
            path = []
            note = ""
            try:
                result = ALL_METHODS[m](problem)
                ms = (time.perf_counter() - start) * 1000
                if m == "ALL":
                    status, note, cost = validate_all(problem, result, exp)
                else:
                    status, note, cost = validate(problem, m, result, exp)
                if isinstance(result, tuple) and len(result) == 3:
                    goal, nodes, path = result
            except NotImplementedError:
                ms, status = 0.0, "TODO"
            except Exception as e:  # a crash is reported, never hidden
                ms, status, note = 0.0, "ERROR", f"{type(e).__name__}: {e}"
            counts[status] += 1
            target = exp["visit_all_cost"] if m == "ALL" else exp["optimal_cost"]
            is_opt = ""
            if cost is not None and target is not None:
                is_opt = "yes" if abs(cost - target) < 1e-9 else "no"
            rows.append([base, m, status, goal, nodes, cost, target, is_opt,
                         " ".join(map(str, path)), round(ms, 3), note])
            if status != "TODO":
                print(f"{base:<34}{m:<7}{status:<7}{str(goal):<6}{str(nodes):<7}{str(cost):<7}{is_opt:<9}{ms:<8.2f}{note}")

    if args.cli:
        print("\nCLI output format (first test file):")
        for m in methods:
            if any(r[1] == m and r[2] == "PASS" for r in rows):
                ok, why = check_cli_format(files[0], m)
                print(f"  {m:<6}{'OK' if ok else 'FAIL: ' + why}")
                counts["PASS" if ok else "FAIL"] += 1

    with open("results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "method", "status", "goal", "nodes_created", "cost",
                    "optimal_cost", "is_optimal", "path", "ms", "note"])
        w.writerows(rows)

    print("\n" + "  ".join(f"{k}: {v}" for k, v in counts.items()) + "   (details in results.csv)")
    sys.exit(1 if counts["FAIL"] or counts["ERROR"] else 0)


if __name__ == "__main__":
    main()