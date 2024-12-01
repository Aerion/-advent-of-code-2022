#!/usr/bin/env python

from aocd import puzzle

data = puzzle.input_data

print(f"Puzzle #{puzzle.day}")
print("--------")
print(f"{data=}")
print("--------")

result = 0

left_list = []
right_list = []
for line in data.splitlines():
    items = line.split()
    left_list.append(int(items[0]))
    right_list.append(int(items[-1]))

left_list.sort()
right_list.sort()

for idx, left in enumerate(left_list):
    right = right_list[idx]
    result += abs(left - right)

print(f"{result=}")