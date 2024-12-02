#!/usr/bin/env python

from aocd import puzzle

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def check(level, prev, is_increasing):
    diff = abs(level - prev)
    if diff < 1 or diff > 3:
        return False

    if not ((is_increasing and level > prev) or (not is_increasing and level < prev)):
        return False

    return True

def check_levels(levels, invalid_count):
    print(levels, invalid_count)
    is_increasing = levels[0] < levels[1]
    prev = levels[0]
    idx = 1
    for level in levels[1:]:
        if not check(level, prev, is_increasing):
            invalid_count += 1
            if invalid_count > 1:
                return False
            return check_levels(levels[0:idx] + levels[idx + 1:], invalid_count) or check_levels(levels[1:], invalid_count) or check_levels(levels[0:idx-1] + levels[idx:], invalid_count)
    
        prev = level
        idx += 1

    return True

result = 0
for line in data.splitlines():
    levels = [*map(int, line.split())]
    if check_levels(levels, 0):
        result += 1

print(f"Result: {result}")