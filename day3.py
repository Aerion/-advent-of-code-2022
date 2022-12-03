import sys

def compute_priority(char):
    if char <= 'Z':
        return ord(char) - ord('A') + 1 + 26

    return ord(char) - ord('a') + 1

priorities_sum = 0
while line := sys.stdin.readline():
    line = line.strip()

    first_rucksack = line[0 : len(line) // 2]
    second_rucksack = line[len(line) // 2 :]
    seen_chars = set(first_rucksack)
    for char in second_rucksack:
        if char in seen_chars:
            priorities_sum += compute_priority(char)
            break

print(priorities_sum)
