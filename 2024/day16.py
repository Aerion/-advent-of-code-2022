#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict
import heapq

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

map = []
start = None
end = None
for y, row in enumerate(data.splitlines()):
    map.append([])
    for x, char in enumerate(row):
        if char == "S":
            start = (x, y)
            char = "."
        elif char == "E":
            end = (x, y)
            char = "."
        map[-1].append(char)


directions = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

def print_map(map, path = []):
    pos_by_dir_idx = {
        0: ">",
        1: "v",
        2: "<",
        3: "^"
    }
    dirs_by_pos = {(x, y): pos_by_dir_idx[dir_idx] for (x, y, dir_idx) in path}
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            print(dirs_by_pos.get((x, y), char), end="")
        print()

q = []
heapq.heappush(q, (0, *start, 0, []))
result = 1000000000000000000000 * len(map) * len(map)
result_paths = set()
score_by_visited = {}
while q:
    score, x, y, dir_idx, path = heapq.heappop(q)
    if score > score_by_visited.get((x, y, dir_idx), 99999999999999999999999999):
        continue
    score_by_visited[(x, y, dir_idx)] = score
    if score > result:
        continue
    if map[y][x] == "#":
        continue
    if (x, y) == end:
        print(score)
        #print_map(map, path)
        if score < result:
            result_paths = set()
            result = score
        if result == score:
            for item in path:
                result_paths.add((item[0], item[1]))
        continue
    #print(score, x, y, dir_idx)
    #print_map(map, path)

    heapq.heappush(q, (score + 1, x + directions[dir_idx][0], y + directions[dir_idx][1], dir_idx, path + [(x, y, dir_idx)]))
    for i in [1, 3]:
        new_dir_idx = (dir_idx + i) % len(directions)
        heapq.heappush(q, (score + 1000, x, y, new_dir_idx, path + [(x, y, new_dir_idx)]))

result = len(result_paths) + 1
print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)