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
'''
data="""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""
data="""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
data = """########
#..O.O.#
#..O@O.#
#...O..#
#.#.O..#
#...O..#
#......#
########

>><<v^<v
"""
data="""#######
#...#.#
#.#O..#
#@O...#
#.....#
#.....#
#######

>>v>>^"""
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
            robot_x = len(map[-1])
            robot_y = y
            char = '.'
        if char == "O":
            map[-1].append("[")
            map[-1].append("]")
        else:
            map[-1].append(char)
            map[-1].append(char)

moves = "".join(moves_str.split("\n"))

def in_bounds(x, y, map):
    return x in range(len(map[0])) and y in range(len(map))

def print_map(map, robot_x, robot_y, move):
    for y, row in enumerate(map):
        line = ""
        for x, char in enumerate(row):
            if y == robot_y and x == robot_x:
                line += move
            else:
                line += char
        print(line)


def push(x, y, x_inc, y_inc, map):
    char = map[y][x]
    if char == "#":
        return False
    if char == ".":
        return True
    
    if x_inc == 0:
        # Vertical push
        map[y][x] = "."
        pair_x = 1 if char == "[" else -1
        pushed = push(x, y + y_inc, x_inc, y_inc, map) and push(x + pair_x, y, x_inc, y_inc, map)
        if pushed:
            map[y + y_inc][x] = char
        else:
            map[y][x] = char
        return pushed
    
    # Horizontal push
    map[y][x] = "."
    map[y][x + x_inc] = "."
    pair_char = "]" if char == "[" else "["
    pushed = push(x + x_inc * 2, y, x_inc, y_inc, map)
    if pushed:
        map[y][x + x_inc] = char
        map[y][x + x_inc * 2] = pair_char
    else:
        map[y][x] = char
        map[y][x + x_inc] = pair_char
    return pushed

for move in moves:
    vector = {
        "<": (-1, 0),
        ">": (1, 0),
        "^": (0, -1),
        "v": (0, 1),
    }[move]
    x_inc, y_inc = vector
    i = 1
    #print(move)
    #print_map(map, robot_x, robot_y, move)

    if map[robot_y + y_inc][robot_x + x_inc] == "#":
        #print_map(map, robot_x, robot_y)
        continue

    if map[robot_y + y_inc][robot_x + x_inc] == ".":
        robot_x += x_inc
        robot_y += y_inc
        #print_map(map, robot_x, robot_y)
        continue

    
    map_copy = [row.copy() for row in map]
    if push(robot_x + x_inc, robot_y + y_inc, x_inc, y_inc, map_copy):
        robot_x += x_inc
        robot_y += y_inc
        map = map_copy
    else:
        map = map
    
print_map(map, robot_x, robot_y, "@")

result = 0
for y, line in enumerate(map):
    for x, char in enumerate(line):
        if char == "[":
            result += 100 * y + x


print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)