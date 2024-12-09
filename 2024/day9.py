#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")


free_list_pos_size: list[tuple[int, int]] = []
file_pos_id_length: list[tuple[int, int, int]] = []

disk_map = []
i = 0
blocks_count = -1
while i < len(data):
    blocks_count += 1
    file_pos_id_length.append((len(disk_map), blocks_count, int(data[i])))
    for x in range(int(data[i])):
        disk_map.append(blocks_count)
    i += 1

    # Free space
    if i >= len(data):
        break

    free_list_pos_size.append((len(disk_map), int(data[i])))
    for x in range(int(data[i])):
        disk_map.append('.')
    i += 1

print(data)
print("".join(str(x) for x in disk_map))
#print(free_list_pos_size)
#print(file_pos_id_length)

for file_pos, file_id, file_length in reversed(file_pos_id_length):
    for free_idx, (free_pos, free_size) in enumerate(free_list_pos_size):
        if free_pos > file_pos:
            # No candidate
            break
        if free_size < file_length:
            # Too small
            continue
        # Found space
        for i in range(file_length):
            disk_map[free_pos + i] = file_id
            disk_map[file_pos + i] = '.'
        
        # Update the size available for the free block
        free_list_pos_size[free_idx] = (free_pos + file_length, free_size - file_length)
        break
    
    #print("".join(str(x) for x in disk_map))
    #print(free_list_pos_size)

print("".join(str(x) for x in disk_map))

result = 0
for left in range(len(disk_map)):
    if disk_map[left] == '.':
        continue
    result += left * disk_map[left]
    

print(f"Result: {result}")
if EXAMPLE_IDX is None:
    submit(result)