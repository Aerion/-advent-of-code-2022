#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

disk_map = []
i = 0
blocks_count = -1
while i < len(data):
    blocks_count += 1
    for x in range(int(data[i])):
        disk_map.append(blocks_count)
    i += 1

    # Free space
    if i >= len(data):
        break

    for x in range(int(data[i])):
        disk_map.append('.')
    i += 1

print(data)
print("".join(str(x) for x in disk_map))

result = 0
left = 0
right = len(disk_map) - 1
while left < right:
    print(left, right)
    if disk_map[left] == '.':
        while disk_map[right] == '.' and left < right:
            right -= 1
            continue
        if left >= right:
            print("It's the end")
            break
        disk_map[left] = disk_map[right]
        disk_map[right] = '.'

    print(left, right)
    result += left * disk_map[left]
    left += 1
    

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)