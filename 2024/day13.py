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
    def is_valid(a, b):
        #print(f"{a=} {b=} {ax * a + bx * b == xtarget=} and {ay * a + by * b == ytarget=}")
        #print(f"{a=} {b=} {ax} * {a} + {bx} * {b} == {xtarget} and {ay} * {a} + {by} * {b} == {ytarget}")
        return ax * a + bx * b == xtarget and ay * a + by * b == ytarget
    
    for i in range(100):
        for j in range(100):
            if is_valid(i, j):
                return i, j
    
    return None, None

result = 0
for i in range(0, len(data), 4):
    a_increment = map(int, [formula.split('+')[1] for formula in data[i].split(',')])
    b_increment = map(int, [formula.split('+')[1] for formula in data[i + 1].split(',')])
    target = map(int, [formula.split('=')[1] for formula in data[i + 2].split(',')])

    a_res, b_res = solve_equation(*a_increment, *b_increment, *target)
    if a_res is not None:
        result += a_res * 3 + b_res

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)