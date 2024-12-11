#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
#data = "125 17"

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def brute_get_stones_after_n_rounds(stones: list[int], rounds_count: int):
    for j in range(rounds_count):
            new_stones = []
            for stone in stones:
                if stone == 0:
                    new_stones.append(1)
                elif len(str(stone)) % 2 == 0:
                    # FAR find better way
                    l = len(str(stone))
                    #print(stone)
                    left = int(str(stone)[0:l//2])
                    right = int(str(stone)[l//2:])
                    new_stones.append(left)
                    new_stones.append(right)
                else:
                    new_stones.append(stone * 2024)
            stones = new_stones
    return stones

future_round_by_stone = {}
#for i in list(range(10)) + [2024]:
    #stones = [i]
    #future_round_by_stone[i] = brute_get_stones_after_n_rounds(stones, 6)

print(future_round_by_stone)

stones_count = defaultdict(int)
for stone in [int(x) for x in data.split()]:
    stones_count[stone] += 1

for i in range(0, 75, 5):
    print(i, stones_count)

    new_stones_count = defaultdict(int)
    for stone, count in stones_count.items():
        if stone not in future_round_by_stone:
            future_round_by_stone[stone] = brute_get_stones_after_n_rounds([stone], 5)
        for new_stone in future_round_by_stone[stone]:
            new_stones_count[new_stone] += count
        
    stones_count = new_stones_count
    #print(stones)

result = sum(stones_count.values())

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)