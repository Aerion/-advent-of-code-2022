#!/usr/bin/env python

from aocd import puzzle

EXAMPLE_IDX = None

VALID_WORD = "MAS"
VALID_CHARS = set(VALID_WORD)

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

map: list[list[str]] = []
for line in data.splitlines():
    map.append([])
    for char in line:
        map[-1].append(char if char in VALID_CHARS else '.')

width = len(map[0])
height = len(map)

def try_get_pos(x, y):
    if y < 0 or y >= height or x < 0 or x >= width:
        return False
    
    return map[y][x]

VALID_MAS_SET = set(('M', 'S'))

def is_valid_a(x, y):
    return (try_get_pos(x, y) == 'A' 
            and set((try_get_pos(x - 1, y - 1), try_get_pos(x + 1, y + 1))) == VALID_MAS_SET
            and set((try_get_pos(x + 1, y - 1), try_get_pos(x - 1, y + 1))) == VALID_MAS_SET
    )

result = 0
for y in range(height):
    for x in range(width):
        if is_valid_a(x, y):
            result += 1

print(f"Result: {result}")