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
for line in data.splitlines():
    mults = re.finditer(r'mul\((\d+),(\d+)\)', line)
    for mult in mults:
        a, b = mult.groups()
        result += int(a)*int(b)

print(f"Result: {result}")