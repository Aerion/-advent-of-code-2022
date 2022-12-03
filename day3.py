from collections import defaultdict
import sys


def compute_priority(char):
    if char <= "Z":
        return ord(char) - ord("A") + 1 + 26

    return ord(char) - ord("a") + 1


priorities_sum = 0
elf_count = 0
seen_chars_group = defaultdict(lambda: 0)
while line := sys.stdin.readline():
    elf_count += 1
    line = line.strip()

    seen_chars = set()
    for char in line:
        if char in seen_chars:
            continue
        seen_chars.add(char)
        seen_chars_group[char] += 1

    if elf_count == 3:
        # Last elf of the group
        for char, count in seen_chars_group.items():
            if count == 3:
                priorities_sum += compute_priority(char)
                elf_count = 0
                seen_chars_group.clear()
                break

print(priorities_sum)
