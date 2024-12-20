#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque
from typing import Optional

EXAMPLE_IDX = 0

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

def print_map(path):
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if (x, y) in path:
                char = "O"
            print(char, end="")
        print()

def build_no_cheat_time_to_end():
    q = deque()
    result = {}
    q.append((*end, 0))

    while q:
        x, y, time = q.popleft()
        if (x, y) not in result:
            result[(x, y)] = time

        for dir_x, dir_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = dir_x + x, dir_y + y
            if (new_x, new_y) in result or new_x < 0 or new_y < 0 or new_x >= len(map[0]) or new_y >= len(map) or map[new_y][new_x] == "#":
                continue
            q.append((new_x, new_y, time + 1))
    
    return result

def dfs(x: int, y: int, time: int, currently_cheating: bool, cheating_time_left: int, cheating_start_pos: Optional[tuple[int, int]], no_cheat_time_to_end: dict[tuple[int, int], int], max_time: int):
    if x < 0 or y < 0 or x >= len(map[0]) or y >= len(map):
        return False
    if time > max_time:
        return False

    if currently_cheating:
        cheating_time_left -= 1
        if cheating_time_left == 0:
            currently_cheating = False

    if map[y][x] == "#":
        assert cheating_start_pos is not None # We should have activated the cheat
        if not currently_cheating:
            # We stopped the cheat before and we're in a wall
            return False
        if cheating_time_left == 0:
            # Can't cheat anymore and we're in a wall
            return False
    
    
    # TODO: handle end
    # TODO: handle already visited

    for dir_x, dir_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x, new_y = dir_x + x, dir_y + y
        if (new_x, new_y) in visited or new_x < 0 or new_y < 0 or new_x >= len(map[0]) or new_y >= len(map):
            continue

def bfs(can_cheat, max_length, distance_to_end, store_path):
    q = deque()
    q.append((*start, 0, can_cheat, 0, set(), [] if store_path else None, None))
    already_used_cheats_start_end = set()
    valid_paths = []
    while q:
        x, y, time, can_disable_time, disable_time_left, visited, path, start_disable_pos = q.popleft()
        new_path = path + [(x,y)] if store_path else None
        #print(x, y, time)
        visited.add((x, y))
        if disable_time_left > 0:
            disable_time_left -= 1
            if disable_time_left == 0:
                key = (start_disable_pos, (x, y))
                if key in already_used_cheats_start_end:
                    print("Skipped (A)")
                    continue
                already_used_cheats_start_end.add(key)

        if max_length and time > max_length:
            continue
        if (x, y) in distance_to_end:
            no_cheat_distance_to_end = distance_to_end[(x, y)]
            if time + no_cheat_distance_to_end < max_length:
                if disable_time_left > 0 and not can_disable_time: # still cheating
                    
                    key = (start_disable_pos, (x, y))
                    if key in already_used_cheats_start_end:
                        print("Skipped (B)")
                        continue
                    already_used_cheats_start_end.add(key)

                print(f"saved {time=}")
                time += no_cheat_distance_to_end
                x, y = end
        if (x, y) == end:
            valid_paths.append((time, new_path))
            if max_length is None:
                break
            continue
        if map[y][x] == "#":
            if disable_time_left <= 0:
                # We can't cheat anymore, stop this path
                continue

        for dir_x, dir_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = dir_x + x, dir_y + y
            if (new_x, new_y) in visited or new_x < 0 or new_y < 0 or new_x >= len(map[0]) or new_y >= len(map):
                continue

            if map[new_y][new_x] == "#" and can_disable_time:
                # Add the node if we disabled the time
                q.append((new_x, new_y, time, False, 14, visited.copy(), new_path, (x, y)))
                continue

            q.append((new_x, new_y, time + 1, can_disable_time, disable_time_left, visited, new_path, start_disable_pos))
    return valid_paths

start_length, default_path = bfs(False, None, {}, True)[0]
print(f"{start_length=}")
no_cheat_time_to_end = build_no_cheat_time_to_end()
#print(len(no_cheat_time_to_end), no_cheat_time_to_end)
#print()
print(sorted(no_cheat_time_to_end.items(), key=lambda x: x[1]))
max_length = start_length - (77 if EXAMPLE_IDX == 0 else 100)
save_path = EXAMPLE_IDX == 0

cheats = bfs(True, max_length, no_cheat_time_to_end, save_path)
if EXAMPLE_IDX == 0:
    for length, path in cheats:
        print()
        print()
        print_map(path)

valid_cheats = [start_length - x[0] for x in cheats]
valid_cheats.sort()
print(valid_cheats)
result = len(valid_cheats)

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)