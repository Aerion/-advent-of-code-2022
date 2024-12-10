#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict
from dataclasses import dataclass

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

'''
data = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""
data ="""..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""
data = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"""
data="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
data="""8901....
7812....
8743.965
96549874
456789.3
32.19.12
.13298.1
1.456732"""

data =""".....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9...."""
data = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""'''
print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def explore(x, y, map, visited, candidate):
    if x < 0 or y < 0 or x >= len(map[0]) or y >= len(map):
        return 0
    if map[y][x] == candidate:
        print(candidate, x, y)
        if map[y][x] == 9:
            visited.add((x, y))
            return 1
        return explore(x + 1, y, map, visited, candidate + 1) + explore(x - 1, y, map, visited, candidate + 1) + explore(x, y + 1, map, visited, candidate + 1) + explore(x, y - 1, map, visited, candidate + 1)
    return 0

result = 0

map = [[int(x) if x.isdigit() else None for x in line] for line in data.splitlines()]
for y, row in enumerate(map):
    for x, char in enumerate(row):
        if char == 0:
            visited = set()
            result += explore(x, y, map, visited, 0)
            # result += len(visited)
            print(result)


for y, row in enumerate(map):
    print("".join("." if v is None else str(v) for x,v in enumerate(row)))

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)