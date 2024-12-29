#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import timedelta
from functools import cache
from rich import print
from sys import stderr
from typing import Optional
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

WIDTH = 3 if EXAMPLE_IDX == 0 else 25
HEIGHT = 2 if EXAMPLE_IDX == 0 else 6
layers_count = len(data) // (WIDTH * HEIGHT)
assert len(data) % (WIDTH * HEIGHT) == 0

def get_val(layer_idx: int, x: int, y: int):
    start_layer = layer_idx * (WIDTH * HEIGHT)
    pos = start_layer + y * WIDTH + x
    return data[pos]

min_layer_idx = None
min_layer_zero_digits_count = WIDTH * HEIGHT

if EXAMPLE_IDX == 0:
    for layer_idx in range(layers_count):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                print(get_val(layer_idx, x, y), end="")
            print()
        print()


for layer_idx in range(layers_count):
    zero_digits_count = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if get_val(layer_idx, x, y) == "0":
                zero_digits_count += 1

    if zero_digits_count > 0 and zero_digits_count < min_layer_zero_digits_count:
        min_layer_idx = layer_idx
        min_layer_zero_digits_count = zero_digits_count

res_one_digit_count = 0
res_two_digit_count = 0
for y in range(HEIGHT):
    for x in range(WIDTH):
        val = get_val(min_layer_idx, x, y)
        if val == "1":
            res_one_digit_count += 1
        elif val == "2":
            res_two_digit_count += 1

result = res_one_digit_count * res_two_digit_count

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if result is not None and EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)