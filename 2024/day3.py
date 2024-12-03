#!/usr/bin/env python

from aocd import puzzle
import re

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

result = 0
enabled = True
for line in data.splitlines():
    for i in range(len(line)):
        item = line[i:i+15]
        if item.startswith("do()"):
            enabled = True
            continue
        if item.startswith("don't()"):
            enabled = False
            continue
        match = re.match(r'mul\((\d{1,3}),(\d{1,3})\)', item)
        if match and enabled:
            a, b = map(int, match.groups())
            result += a*b

print(f"Result: {result}")