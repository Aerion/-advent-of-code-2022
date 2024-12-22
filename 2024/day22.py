#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    data = """1
10
100
2024"""

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def get_secret(secret):
    secret = prune(mix(secret << 6, secret))
    print(secret)
    secret = prune(mix(secret >> 5, secret))
    print(secret)
    secret = prune(mix(secret << 11, secret))
    print(secret)
    return secret

def mix(value, secret):
    return value ^ secret

def prune(secret):
    return secret & (2 ** 24)

result = 0
for line in data.splitlines():
    secret = int(line)
    for i in range(2000):
        first = ((secret * 64) ^ secret) % 16777216
        #print(first)
        second = ((first // 32) ^ first) % 16777216
        #print(second)
        third = ((second * 2048) ^ second) % 16777216
        #print(third)
        #print("now other")
        secret = third
        #secret = get_secret(secret)
        #print(secret)
    #exit(0)
    result += secret

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)