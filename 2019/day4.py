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

PWD_LEN = 6
MIN, MAX = map(int, data.split("-"))

def fill_passwords(prefix: str, previous_digit: int, passwords: set[int]):
    if len(prefix) == PWD_LEN:
        if not MIN <= int(prefix) <= MAX:
            return
        for i in range(len(prefix) - 1):
            prev = None if i == 0 else prefix[i - 1]
            next = None if i == len(prefix) - 2 else prefix[i + 2]
            if prefix[i + 1] == prefix[i] and prefix[i] != prev and prefix[i] != next:
                # There is adjacency
                passwords.add(prefix)
                return

        # No adjacency
        return

    for i in range(previous_digit, 10):
        fill_passwords(f"{prefix}{i}", i, passwords)

passwords = set()
fill_passwords("", 1, passwords)
result = len(passwords)

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if result is not None and EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)