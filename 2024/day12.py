#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

'''
data = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
data="""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
'''
print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def in_bounds(x: int, y: int, map: list[list[str]]):
    return x >= 0 and y >= 0 and x < len(map[0]) and y < len(map)

def get_zone_score(x: int, y: int, map: list[list[str]], plot: str, visited: set):
    if not in_bounds(x, y, map) or map[y][x] != plot:
        # Increase perimeter by 1
        return 0, 1
    
    # Vist the node
    map[y][x] = '.'
    visited.add((x, y))
    
    # Increase area by 1
    area, perimeter = 1, 0
    
    for new_x, new_y in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if (new_x, new_y) in visited:
            continue
        area_delta, perimeter_delta = get_zone_score(new_x, new_y, map, plot, visited)
        area += area_delta
        perimeter += perimeter_delta
    
    return area, perimeter
    

map = [[x for x in line] for line in data.splitlines()]

def print_map():
    for line in map:
        print("".join(line))

result = 0
for y, line in enumerate(map):
    for x, plot in enumerate(line):
        if plot == '.':
            continue
        visited = set()
        area, perimeter = get_zone_score(x, y, map, plot, visited)
        result += area * perimeter
        print(area, perimeter, result)
        print_map()

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)