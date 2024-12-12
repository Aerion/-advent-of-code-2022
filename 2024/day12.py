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


FENCE_BY_DIRECTION = {
    (1, 0): '}',
    (-1, 0): '{',
    (0, 1): '_',
    (0, -1): '-',
}

OPPOSITE_DIRECTION = {
    (1, 0): (-1, 0),
    (-1, 0): (1, 0),
    (0, 1): (0, -1),
    (0, -1) : (0, 1)
}

def get_zone_score(x: int, y: int, map: list[list[str]], plot: str, visited: set, visited_dir: set, direction: tuple[int, int], fences: dict[tuple[int, int], set[str]]):
    #print(x,y)
    if not in_bounds(x, y, map) or map[y][x] != plot:
        # Increase perimeter by 1
        return 0, 1
    
    # Vist the node
    visited_dir.add((x, y, direction))

    already_visited = (x, y) in visited
    visited.add((x, y))

    # Increase area by 1
    area, perimeter = 1, 0
    
    for new_direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if not already_visited:
            fences[x, y].add(FENCE_BY_DIRECTION[new_direction])

    for new_direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        new_x, new_y = (new_direction[0] + x, new_direction[1] + y)
        if (new_x, new_y, new_direction) in visited_dir:
            continue
        area_delta, perimeter_delta = get_zone_score(new_x, new_y, map, plot, visited, visited_dir, new_direction, fences)
        area += area_delta
        perimeter += perimeter_delta

        #print(f"Checking {new_x} {new_y} from {x} {y}")
        if area_delta > 0:
            # We found another plot, remove the fence
            #print(f"Found another plot, remove {FENCE_BY_DIRECTION[new_direction]} from {x} {y} (with existing {fences[x, y]}) and remove {FENCE_BY_DIRECTION[OPPOSITE_DIRECTION[new_direction]]} from {new_x} {new_y}")
            if FENCE_BY_DIRECTION[new_direction] in fences[x, y]:
                fences[x, y].remove(FENCE_BY_DIRECTION[new_direction])
            if FENCE_BY_DIRECTION[OPPOSITE_DIRECTION[new_direction]] in fences[new_x, new_y]:
                fences[new_x, new_y].remove(FENCE_BY_DIRECTION[OPPOSITE_DIRECTION[new_direction]])
    
    map[y][x] = '.'
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
        visited_dir = set()
        fences = defaultdict(set)
        area, perimeter = get_zone_score(x, y, map, plot, visited, visited_dir, (1, 0), fences)
        area = len(visited)

        #print(area, perimeter, result)
        #print(fences)
        #print_map()

        positions_by_fence_kind: dict[dict[list[int], int], str] = {}
        for pos in fences:
            for fence in fences[pos]:
                if fence not in positions_by_fence_kind:
                    positions_by_fence_kind[fence] = defaultdict(list[int])
                if fence == '}' or fence == '{':
                    key, value = pos[0], pos[1]
                else:
                    key, value = pos[1], pos[0]
                positions_by_fence_kind[fence][key].append(value)

        #print(positions_by_fence_kind)

        total_sides_count = 0
        for fence_kind, candidates_group in positions_by_fence_kind.items():
            sides_count = 0

            for candidates in candidates_group.values():
                fence_sides_count = 1
                candidates.sort()
                #print(candidates)
                for i in range(1, len(candidates)):
                    if candidates[i - 1] + 1 != candidates[i]:
                        fence_sides_count += 1
                sides_count += fence_sides_count
            #print(f"{fence_kind} has {sides_count} sides for plot {plot}")
            total_sides_count += sides_count

        region_price = area * total_sides_count
        print(f"Plot {plot} has {total_sides_count} sides with area {area} => ${region_price}")

        result += region_price

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)