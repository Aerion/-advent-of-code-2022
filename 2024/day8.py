#!/usr/bin/env python

from aocd import puzzle
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

'''
data ="""..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
.........."""
data = """..........
..........
..........
....a.....
........a.
.....a....
..........
......A...
..........
.........."""'''

def in_bounds(x, y, map):
    return x >= 0 and y >= 0 and x < len(map[0]) and y < len(map)

def get(x, y, map):
    if not in_bounds(x, y, map):
        return None
    return map[y][x]

map = [[x for x in line] for line in data.splitlines()]
antenna_positions: dict[list[tuple[int, int]]] = defaultdict(list)

result = 0
for y, row in enumerate(map):
    for x, char in enumerate(row):
        if (char == '.'):
            continue
        antenna_positions[char].append((x, y))

print("\n".join("".join(x for x in line) for line in map) + "\n")
antinodes = set()
for antenna, positions in antenna_positions.items():
    for i, pos in enumerate(positions):
        for j, next_pos in enumerate(positions[:i] + positions[i + 1:]):
            pos_diff = (next_pos[0] - pos[0], next_pos[1] - pos[1])

            first_antenna_pos = (pos_diff[0] + next_pos[0], pos_diff[1] + next_pos[1])
            next_antenna_pos = (pos[0] - pos_diff[0], pos[1] - pos_diff[1])

            print(antenna, pos, next_pos)
            print(first_antenna_pos, next_antenna_pos)
            
            old_res = result

            if in_bounds(*first_antenna_pos, map) and first_antenna_pos not in antinodes:
                result += 1
                antinodes.add(first_antenna_pos)
            if in_bounds(*next_antenna_pos, map) and next_antenna_pos not in antinodes:
                result += 1
                antinodes.add(next_antenna_pos)
            
            if result != old_res:
                print("\n".join("".join(x for x in line) for line in map) + "\n")
                pass

print(f"Result: {result}")