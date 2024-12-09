#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = 0

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

result = 0
for line in data.splitlines():
    pass

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)