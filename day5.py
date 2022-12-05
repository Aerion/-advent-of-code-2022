import sys
import re

line = sys.stdin.readline()
stacks_count = int((len(line) + 1) / 4)
stacks = []
for _ in range(stacks_count):
    stacks.append([])
while line:
    if line[1] == "1":
        break
    for i in range(stacks_count):
        item = line[i * 4 + 1]
        if item == ' ':
            continue
        if not stacks[i]:
            stacks[i] = []
        stacks[i].insert(0, item)

    line = sys.stdin.readline()

# Empty line delimiting stacks from moves
sys.stdin.readline()

while line := sys.stdin.readline():
    line = line.strip()
    matches = re.match(r'move (\d+) from (\d+) to (\d+)', line)

    count = int(matches.group(1))
    original_stack = int(matches.group(2)) - 1
    final_stack = int(matches.group(3)) - 1

    for _ in range(count):
        stacks[final_stack].append(stacks[original_stack].pop())


for stack in stacks:
    print(stack.pop(), end='')