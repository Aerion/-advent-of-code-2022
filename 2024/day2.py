#!/usr/bin/env python

from aocd import puzzle

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

result = []
for line in data.splitlines():
    levels = [*map(int, line.split())]

    is_valid = True
    is_increasing = levels[0] < levels[1]
    prev = levels[0]
    for level in levels[1:]:
        diff = abs(level - prev)

        if diff < 1 or diff > 3:
            print(diff)
            is_valid = False
            break

        if not ((is_increasing and level > prev) or (not is_increasing and level < prev)):
            print(prev, level, is_increasing)
            is_valid = False
            break
    
        prev = level

    if is_valid:
        result.append(levels)

print(f"Result: {len(result)}")