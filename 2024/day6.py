#!/usr/bin/env python

from aocd import puzzle
from enum import Enum

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")


class Direction(Enum):
    Top = 0,
    Right = 1,
    Bottom = 2,
    Left = 3,

directions = [Direction.Top, Direction.Right, Direction.Bottom, Direction.Left]
vector_by_direction = {
    Direction.Top: (0, -1),
    Direction.Right: (1, 0),
    Direction.Bottom: (0, 1),
    Direction.Left: (-1, 0)
}

result = 0

start_pos = None

map: list[list[str]] = []
for y, line in enumerate(data.splitlines()):
    map.append([])
    for x, char in enumerate(line):
        if char == '^':
            char = '.'
            start_pos = (x, y)
        map[-1].append(char)

def in_bounds(x, y):
    return x >= 0 and y >= 0 and x < len(map[0]) and y < len(map)

result = 0 # POsitions visited

(x, y) = start_pos
direction_idx = 0
while True:
    if map[y][x] == ".":
        map[y][x] = "X"
        result += 1

    (x_inc, y_inc) = vector_by_direction[directions[direction_idx]]
    next_x = x + x_inc
    next_y = y + y_inc

    if not in_bounds(next_x, next_y):
        # The end
        break

    if map[next_y][next_x] == "#":
        direction_idx = (direction_idx + 1) % len(directions)
        continue
    
    x = next_x
    y = next_y

    #print("\n".join("".join(line) for line in map))
    #print("")

print(f"Result: {result}")