#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None
HEIGHT = 103
WIDTH = 101

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

robots = []
for line in data.splitlines():
    elms = line.split(' ')
    pos = [int(x) for x in elms[0].split('=')[1].split(',')]
    velocity = [int(x) for x in elms[1].split('=')[1].split(',')]
    robots.append((pos, velocity))

def get_new_pos(pos, velocity, duration):
    return ((pos[0] + (velocity[0] * duration) + WIDTH) % WIDTH, (pos[1] + (velocity[1] * duration) + HEIGHT) % HEIGHT)

for duration in range(99999999999999999):
    unique_pos = set()
    
    for pos, velocity in robots:
        new_pos = get_new_pos(pos, velocity, duration)
        if 20 < new_pos[1] < 40:
            unique_pos.add(new_pos)

    if len(unique_pos) > .3 * len(robots):
        table = []
        for n in range(HEIGHT):
            table += [['.'] * WIDTH]
        for pos, velocity in robots:
            new_pos = get_new_pos(pos, velocity, duration)
            table[new_pos[1]][new_pos[0]] = '#'
        print(duration, len(unique_pos))
        for n in range(HEIGHT):
            print("".join(table[n]))
        print("\n\n\n\n\n")

        from time import sleep
        sleep(0.05)

"""
print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)"""