#!/usr/bin/env python

from aocd import puzzle
from collections import defaultdict

data = puzzle.input_data

print(f"Puzzle #{puzzle.day}")
print("--------")
print(f"{data=}")
print("--------")

result = 0

left_list = []
right_list_frequency = defaultdict(int)
for line in data.splitlines():
    items = line.split()
    left_list.append(int(items[0]))

    right = int(items[-1])
    right_list_frequency[right] += 1

for left in left_list:
    result += left * right_list_frequency[left]

print(f"{result=}")