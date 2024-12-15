#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
'''
data="""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
'''

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")


map_str, moves_str = data.split('\n\n')

robot_x = 0
robot_y = 0
map: list[list[str]] = []
for y, row in enumerate(map_str.splitlines()):
    map.append([])
    for x, char in enumerate(row):
        if char == '@':
            robot_x = x
            robot_y = y
            char = '.'
        map[-1].append(char)

moves = "".join(moves_str.split("\n"))

def in_bounds(x, y, map):
    return x in range(len(map[0])) and y in range(len(map))

def print_map(map, robot_x, robot_y):
    for y, row in enumerate(map):
        line = ""
        for x, char in enumerate(row):
            if y == robot_y and x == robot_x:
                line += "@"
            else:
                line += char
        print(line)

for move in moves:
    vector = {
        "<": (-1, 0),
        ">": (1, 0),
        "^": (0, -1),
        "v": (0, 1),
    }[move]
    x_inc, y_inc = vector
    i = 1

    if map[robot_y + y_inc][robot_x + x_inc] == ".":
        robot_x += x_inc
        robot_y += y_inc
        continue
    
    while map[robot_y + y_inc * i][robot_x + x_inc * i] not in ["#", "."]:
        i += 1
    # Stop before the wall
    if map[robot_y + y_inc * i][robot_x + x_inc * i] == "#":
        i -= 1

    if i == 0:
        # Against a wall, nothing to do
        continue
    if map[robot_y + y_inc * i][robot_x + x_inc * i] == ".":
        # We can push the elements around
        map[robot_y + y_inc * i][robot_x + x_inc * i], map[robot_y + y_inc][robot_x + x_inc] = map[robot_y + y_inc][robot_x + x_inc], map[robot_y + y_inc * i][robot_x + x_inc * i]
        robot_x += x_inc
        robot_y += y_inc
    
print_map(map, robot_x, robot_y)

result = 0
for y, line in enumerate(map):
    for x, char in enumerate(line):
        if char == "O":
            result += 100 * y + x


print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)