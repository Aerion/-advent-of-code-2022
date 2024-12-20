#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")


map = []
start, end = None, None
for y, line in enumerate(data.splitlines()):
    map.append([])
    for x, char in enumerate(line):
        if char == "S":
            start = (x, y)
        elif char == "E":
            end = (x, y)
        map[-1].append(char)

def bfs(can_cheat, max_length, distance_to_end, store_path):
    q = deque()
    q.append((*start, 0, can_cheat, 0, set(), [] if store_path else None))
    valid_paths = []
    while q:
        x, y, time, can_disable_time, disable_time_left, visited, path = q.popleft()
        new_path = path + [(x,y)] if store_path else None
        #print(x, y, time)
        visited.add((x, y))
        if disable_time_left > 0:
            disable_time_left -= 1
        if max_length and time > max_length:
            continue
        if (x, y) in distance_to_end:
            no_cheat_distance_to_end = distance_to_end[(x, y)]
            if time + no_cheat_distance_to_end < max_length:
                print(f"saved {time=}")
                time += no_cheat_distance_to_end
                x, y = end
        if (x, y) == end:
            valid_paths.append((time, new_path))
            if max_length is None:
                break
            continue
        if map[y][x] == "#":
            if can_disable_time:
                # Add the node if we disabled the time
                q.append((x, y, time, False, 2, visited.copy(), new_path))
                continue
            if disable_time_left <= 0:
                # We can't cheat anymore, stop this path
                continue

        for dir_x, dir_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = dir_x + x, dir_y + y
            if (new_x, new_y) in visited or new_x < 0 or new_y < 0 or new_x >= len(map[0]) or new_y >= len(map):
                continue
            q.append((new_x, new_y, time + 1, can_disable_time, disable_time_left, visited, new_path))
    return valid_paths

start_length, default_path = bfs(False, None, {}, True)[0]
print(f"{start_length=}")
#print(f"{default_path=}")
distance_to_end = {pos: i for i, pos in enumerate(reversed(default_path))}
#print(distance_to_end)
max_length = start_length - (0 if EXAMPLE_IDX == 0 else 100)
valid_cheats = [start_length - x[0] for x in bfs(True, max_length, distance_to_end, False)]
valid_cheats.sort()
print(valid_cheats)
result = len(valid_cheats)

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)