#!/usr/bin/python

import sys

cur_elf_calories = 0
max_elf_calories = 0
while line := sys.stdin.readline():
    line = line.strip()
    if not line:
        max_elf_calories = max(cur_elf_calories, max_elf_calories)
        cur_elf_calories = 0
        continue

    value = int(line)
    cur_elf_calories += value

print(max_elf_calories)
