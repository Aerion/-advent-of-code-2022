#!/usr/bin/env python

from aocd import puzzle
from enum import Enum

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

'''
data = """.#..#...
#......#
...#....
#.......
.^#....."""

data = """...#
...#
...#
#^.#
..#."""

data = """.#.#
#..#
#..#
#^.#
...."""

data = """....
...#
#...
.^#."""

data = """#..#
#..#
#.##
#..#
#..#
#^#.
.#.."""

data = """...
#^#
.#."""

data = """...
.^#
#..
.#."""
'''

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")


class Direction(Enum):
    Top = "^",
    Right = ">",
    Bottom = "v",
    Left = "<",

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

def print_map(map):
    print("\n".join("".join(line) for line in map))
    print("")

LOOP_FOUND = -1
ESCAPED = -2

import sys
sys.setrecursionlimit(50000)

already_evaluated_lines = set()

def explore(x: int, y: int, direction_idx: int, obstacle_set: bool, map: list[list[str]], directions_visited_by_pos: dict[tuple[int, int], list[Direction]], result: int):
    map[y][x] = str(directions[direction_idx].value[0])
    #print(obstacle_set, y, x)
    #print_map(map)
    
    if (x, y) not in directions_visited_by_pos:
        directions_visited_by_pos[(x, y)] = []
    
    if directions[direction_idx] in directions_visited_by_pos[(x, y)]:
        # We're in a loop
        if not obstacle_set:
            print("Looping without obstacle")
            exit(42)

        # loop found
        return 1

    directions_visited_by_pos[(x, y)].append(directions[direction_idx])

    (x_inc, y_inc) = vector_by_direction[directions[direction_idx]]
    next_x = x + x_inc
    next_y = y + y_inc

    if not in_bounds(next_x, next_y):
        # The end
        #print("bye bye")
        return result

    if map[next_y][next_x] == "#" or map[next_y][next_x] == "O":
        # change direction
        direction_idx = (direction_idx + 1) % len(directions)
        return explore(x, y, direction_idx, obstacle_set, map, directions_visited_by_pos, result)

    # We can set an obstacle where we never went only
    if map[next_y][next_x] == "." and not obstacle_set:
        # Simulate if we put an obstacle at the point

        potential_next_direction_idx = (direction_idx + 1) % len(directions)
        potential_next_increments = vector_by_direction[directions[potential_next_direction_idx]]
        potential_next_x, potential_next_y = (x + potential_next_increments[0], y + potential_next_increments[1])

        #print_map(map)

        if in_bounds(potential_next_x, potential_next_y) and map[next_y][next_x] != "#":
            # Backup
            old_directions_visited_by_pos = {k: directions_visited_by_pos[k].copy() for k in directions_visited_by_pos}
            old_map = [row.copy() for row in map]

            # Set the obstacle
            map[next_y][next_x] = 'O'
            loops_count = explore(x, y, potential_next_direction_idx, True, map, directions_visited_by_pos, 0)
            if loops_count > 0:
                #print(f"{loops_count} LOOPS FOUND BY PUTTING AT {next_x}, {next_y}")
                #print_map(map)
                # Found a loop with this obstacle
                result += loops_count

            # Restore
            map = old_map
            directions_visited_by_pos = old_directions_visited_by_pos
        else:
            print(f"Won't explore because {in_bounds(potential_next_x, potential_next_y)=} {map[potential_next_y][potential_next_x]=}")
            print(potential_next_x, potential_next_y)
    
    return explore(next_x, next_y, direction_idx, obstacle_set, map, directions_visited_by_pos, result)

result = explore(start_pos[0], start_pos[1], 0, False, map, {}, 0)

print(f"Result: {result}")