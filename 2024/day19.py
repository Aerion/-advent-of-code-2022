#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict
import re
from tqdm import tqdm

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

s1, s2 = data.split("\n\n")
available_towels = [s.strip() for s in s1.split(",")]

def is_possible(line, towels):
    return re.match("^(" + "|".join(towels) + ")+$", line) != None

BASE_TOWELS = ["w", "u", "b", "r", "g"]
base_towels_present = [towel for towel in BASE_TOWELS if towel in available_towels]

# Filter out all the useless towels as they can be constructed with the base ones
useful_towels = [towel for towel in available_towels if len(towel) == 1 or all(x for x in towel if x in base_towels_present)]

print(len(available_towels), "towels reduced to", len(useful_towels))
useful_towels_by_length = defaultdict(list)
max_towel_length = 0
for towel in useful_towels:
    useful_towels_by_length[len(towel)].append(towel)
    max_towel_length = max(len(towel), max_towel_length)

print(useful_towels)

reduced_useful_towels = []
for i in range(max_towel_length + 1):
    for towel in useful_towels_by_length[i]:
        sub_towels = []
        for j in range(i - 1, 0, -1):
            sub_towels.extend(useful_towels_by_length[j])
        if towel == "bwu":
            print(sub_towels)
        if is_possible(towel, sub_towels):
            # This can be constructed with smaller towels
            continue
        reduced_useful_towels.append(towel)

print(len(useful_towels), "towels reduced to", len(reduced_useful_towels))

reduced_useful_towels.sort(key=lambda x: len(x), reverse=True)
print(reduced_useful_towels)

result = 0
for line in tqdm(s2.splitlines()):
    if is_possible(line, reduced_useful_towels):
        result += 1

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)