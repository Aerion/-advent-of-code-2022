#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
#data = "125 17"

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

stones = [int(x) for x in data.split()]
for i in range(25):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            # FAR find better way
            l = len(str(stone))
            #print(stone)
            left = int(str(stone)[0:l//2])
            right = int(str(stone)[l//2:])
            new_stones.append(left)
            new_stones.append(right)
        else:
            new_stones.append(stone * 2024)
    stones = new_stones
    #print(stones)

result = len(stones)

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)