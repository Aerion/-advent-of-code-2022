#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict
from functools import cache

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

s1, s2 = data.split("\n\n")
towels = set(s.strip() for s in s1.split(","))

max_towel_length = max(len(towel) for towel in towels)
        
@cache
def get_possibilities_count(line: str):
    valid_variations = 0

    for towel in towels:
        if towel == line:
            # Finished it, it's a proper variation!
            valid_variations += 1
            continue
        if line.startswith(towel):
            valid_variations += get_possibilities_count(line[len(towel):])
    
    return valid_variations

result = 0
for line in s2.splitlines():
    count = get_possibilities_count(line)
    print(f"{line=} {count=}")
    result += count

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)