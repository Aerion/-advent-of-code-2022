#!/usr/bin/python

import sys

cur_elf_calories = 0
top_3_elf_calories = [0, 0, 0]
while line := sys.stdin.readline():
    line = line.strip()
    if not line:
        if cur_elf_calories > top_3_elf_calories[0]:
            top_3_elf_calories = [cur_elf_calories] + top_3_elf_calories[1:]
            top_3_elf_calories.sort()

        cur_elf_calories = 0
        continue

    value = int(line)
    cur_elf_calories += value

print(sum(top_3_elf_calories))
