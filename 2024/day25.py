#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None
KEY_LEN = 5

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    # Override data if needed
    pass

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def compute_heights(lines: list[str], is_key: bool):
    heights = []
    needle = "#"
    for x in range(KEY_LEN):
        needle_pos = 0
        for j in sorted(range(1, KEY_LEN + 1), reverse=not is_key):
            if lines[j][x] == needle:
                if is_key:
                    needle_pos = KEY_LEN + 1 - j
                else:
                    needle_pos = j
                break
        heights.append(needle_pos)
    return tuple(heights)


keys = []
locks = []
for lines in [x.splitlines() for x in data.split("\n\n")]:
    if lines[0] == "." * KEY_LEN:
        # Key
        assert lines[-1] == "#" * KEY_LEN
        keys.append(compute_heights(lines, True))
    else:
        assert lines[0] == "#" * KEY_LEN
        assert lines[-1] == "." * KEY_LEN
        locks.append(compute_heights(lines, False))

result = 0
for lock in locks:
    for key in keys:
        print(lock, key)
        valid = True
        for i in range(KEY_LEN):
            if lock[i] + key[i] > KEY_LEN:
                valid = False
                break
        if valid:
            result += 1
        else:
            print("overlaps on", i)

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)