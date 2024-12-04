#!/usr/bin/env python

from aocd import puzzle
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    BOTTOM_LEFT = 5
    BOTTOM_RIGHT = 6
    TOP_LEFT = 7
    TOP_RIGHT = 8

DIRECTION_VECTORS = {
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
    Direction.TOP: (0, -1),
    Direction.BOTTOM: (0, 1),
    Direction.BOTTOM_LEFT: (1, -1),
    Direction.BOTTOM_RIGHT: (1, +1),
    Direction.TOP_LEFT: (-1, -1),
    Direction.TOP_RIGHT: (-1, 1),
}

EXAMPLE_IDX = None

VALID_WORD = "XMAS"
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

from pprint import pprint
pprint(map)

def search_xmas(x, y, valid_length, direction: Direction):
    # print(x, y, valid_length)
    if y < 0 or y >= height or x < 0 or x >= width:
        return 0
    if map[y][x] != VALID_WORD[valid_length]:
        return 0

    new_valid_length = valid_length + 1
    if new_valid_length == len(VALID_WORD):
        print(x, y, map[y][x], valid_length, VALID_WORD[valid_length])
        # Found it
        return 1
    
    # Still on the search
    inc_x, inc_y = DIRECTION_VECTORS[direction]
    return search_xmas(x + inc_x, y + inc_y, new_valid_length, direction)


result = 0

for y in range(height):
    for x in range(width):
        for direction in Direction:
            result += search_xmas(x, y, 0, direction)


print(f"Result: {result}")