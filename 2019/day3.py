#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque
from datetime import timedelta
from functools import cache
from rich import print
from sys import stderr
import time

EXAMPLE_IDX = None
_start_time = time.time()

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    # Override data if needed
    # data = """REPLACE_ME"""
    pass

print(f"Puzzle #{puzzle.day}", file=stderr)

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data", file=stderr)
else:
    print(f"Using PROD data", file=stderr)

#################################################################
# No changes before this line
#################################################################

def print_map(map: dict[tuple[int, int], int]):
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            char = map.get((x, y), '.')
            if char == 3:
                char = f"[bold red]{char}[/]"
            print(char, end="")
        print()

directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "D": (0, 1),
    "U": (0, -1),
}

wires = data.splitlines()
map: dict[tuple[int, int], int] = defaultdict(int)
wire_step_by_pos = [
    {}, {}
]
min_x, min_y, max_x, max_y = 0, 0, 0, 0
for wire_idx, wire in enumerate(wires):
    x, y = 0, 0
    step = 0
    for instruction in wire.split(","):
        length = int(instruction[1:])
        direction = directions[instruction[0]]

        for i in range(length):
            step += 1
            x += direction[0]
            y += direction[1]

            map[(x, y)] |= 1 << wire_idx
            if (x, y) not in wire_step_by_pos[wire_idx]:
                wire_step_by_pos[wire_idx][(x, y)] = step

            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

if EXAMPLE_IDX is not None:
    print_map(map)

min_distance = 2 ** 32
for key, value in map.items():
    if value == 3:
        distance = wire_step_by_pos[0][key] + wire_step_by_pos[1][key]
        min_distance = min(min_distance, distance)

result = min_distance

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if result is not None and EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)