#!/usr/bin/env python

from aocd import puzzle

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def is_valid(cur: int, target: int, numbers: list[int]):
    print(cur, target, numbers)

    if cur == target and not numbers:
        return True

    if cur > target or not numbers:
        return False
    
    n = numbers[0]
    return is_valid(cur * n, target, numbers[1:]) or is_valid(cur + n, target, numbers[1:])

result = 0
for line in data.splitlines():
    items = line.split(':')
    target = int(items[0])
    numbers = [int(item) for item in items[1].split()]

    if is_valid(numbers[0], target, numbers[1:]):
        print(target)
        result += target

print(f"Result: {result}")