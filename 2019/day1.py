#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque
from datetime import timedelta
from functools import cache
from rich import print
from sys import stderr
import time

EXAMPLE_IDX = None
_start_time = time.time()

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    data = """14"""
    # Override data if needed
    pass

print(f"Puzzle #{puzzle.day}", file=stderr)

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data", file=stderr)
else:
    print(f"Using PROD data", file=stderr)

def get_fuel(mass: int):
    return max(0, mass // 3 - 2)

result = 0
for line in data.splitlines():
    mass = int(line)
    while mass > 0:
        fuel = get_fuel(mass)
        result += fuel
        mass = fuel

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)