#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

data = data.splitlines()

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")


def solve_equation(ax, ay, bx, by, xtarget, ytarget):
    # Solve 
    #   ax * a + bx * b == xtarget
    #   ay * a + by * b == ytarget

    b = (-xtarget * ay + ytarget * ax) / (-bx * ay + by * ax)
    a = (xtarget - bx * b) / ax

    return a,b

result = 0
for i in range(0, len(data), 4):
    a_increment = map(int, [formula.split('+')[1] for formula in data[i].split(',')])
    b_increment = map(int, [formula.split('+')[1] for formula in data[i + 1].split(',')])
    target = map(lambda x: 10000000000000 + x, map(int, [formula.split('=')[1] for formula in data[i + 2].split(',')]))

    a_res, b_res = solve_equation(*a_increment, *b_increment, *target)
    if round(a_res) == a_res and round(b_res) == b_res:
        print(f"Round: {a_res} {b_res}")
        result += a_res * 3 + b_res
    else:
        print(f"Not round: {a_res} {b_res}")

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)