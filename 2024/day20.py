#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque
from typing import Optional

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

def print_map(path, jumps = []):
    return
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if (x, y) == start:
                char = "S"
            elif (x, y) == end:
                char = "E"
            elif (x, y) in path:
                char = "O"
            elif (x, y) in jumps:
                char = "J"
            print(char, end="")
        print()
    print()

def build_no_cheat_time_to_end():
    q = deque()
    result = {}
    q.append((*end, 0, [end]))

    while q:
        x, y, time, path = q.popleft()
        if (x, y) not in result:
            result[(x, y)] = time

        for dir_x, dir_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = dir_x + x, dir_y + y
            if (new_x, new_y) in result or new_x < 0 or new_y < 0 or new_x >= len(map[0]) or new_y >= len(map) or map[new_y][new_x] == "#":
                continue
            q.append((new_x, new_y, time + 1, [(new_x, new_y)] + path))
    
    return result, path


def debug(str):
    return
    print(str)

no_cheat_time_to_end, base_path = build_no_cheat_time_to_end()
print_map(base_path)
reversed_base_path = list(reversed(base_path))

CHEATING_MAX_LENGTH = 20
MIN_SAVED_PICOSECONDS = 100

valid_cheat = set()
result = 0
for time, start_cheat_pos in enumerate(base_path):
    found = False
    for i, target in enumerate(reversed_base_path):
        cheat_distance = abs(target[0] - start_cheat_pos[0]) + abs(target[1] - start_cheat_pos[1])
        if cheat_distance <= CHEATING_MAX_LENGTH:
            # Can jump on that one
            cheat_distance -= 1
            time_done = time + cheat_distance
            time_until_end = no_cheat_time_to_end[target]
            total_time = time_done + time_until_end
            saved_time = no_cheat_time_to_end[start] - total_time - 1
            #debug(f"BLabla by jumping from {start_cheat_pos} to {target} ({cheat_distance=}) (saved {saved_time})")
            if saved_time >= MIN_SAVED_PICOSECONDS:
                debug(f"Valid by jumping from {start_cheat_pos} to {target} ({cheat_distance=}) (saved {saved_time}) -- {total_time=} = {time_done=} + {time_until_end=}")
                debug(f"{no_cheat_time_to_end[target]=}")
                debug(f"{no_cheat_time_to_end[start]=}")


                path = base_path[:time + 1] + reversed_base_path[:i + 1]
                debug(path)
                jumps = []

                x_inc = -1 if target[0] < start_cheat_pos[0] else 1
                for x_i in range(abs(target[0] - start_cheat_pos[0]) + 1):
                    jumps.append((start_cheat_pos[0] + x_inc * x_i, target[1]))
                y_inc = -1 if target[0] < start_cheat_pos[0] else 1
                for y_i in range(abs(target[1] - start_cheat_pos[1]) + 1):
                    jumps.append((start_cheat_pos[0], start_cheat_pos[1] + y_inc * y_i))
                debug(jumps)


                print_map(path, jumps)
                result += 1


print(f"{result=}")
#exit(0)

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)