#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None
HEIGHT = 103
WIDTH = 101
#HEIGHT = 7
#WIDTH = 11
DURATION = 100

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
#data ="""p=2,4 v=2,-3"""

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")


robots_count_by_quadrant = defaultdict(int)
for line in data.splitlines():
    elms = line.split(' ')
    pos = [int(x) for x in elms[0].split('=')[1].split(',')]
    velocity = [int(x) for x in elms[1].split('=')[1].split(',')]

    #for DURATION in range(6):
    new_pos = ((pos[0] + (velocity[0] * DURATION) + WIDTH) % WIDTH, (pos[1] + (velocity[1] * DURATION) + HEIGHT) % HEIGHT)
        #print(pos, velocity, new_pos)
    if new_pos[0] == (WIDTH - 1) // 2 or new_pos[1] == (HEIGHT - 1) // 2:
        continue
    
    quadrant_x = 0 if new_pos[0] < ((WIDTH - 1) // 2) else 1
    quadrant_y = 0 if new_pos[1] < ((HEIGHT - 1) // 2) else 1
    robots_count_by_quadrant[(quadrant_x, quadrant_y)] += 1

print(robots_count_by_quadrant)
result = 1
for robots_count in robots_count_by_quadrant.values():
    result *= robots_count

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)