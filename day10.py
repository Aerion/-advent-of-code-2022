import sys

total_signal_strength = 0
cpu_cycle = 1
rx = 1

while line := sys.stdin.readline():
    parts = line.strip().split(' ')
    instruction = parts[0]

    if instruction == "noop":
        cost = 1
    else:
        cost = 2

    for _ in range(cost):
        print(f"{cpu_cycle}: {line.strip()} ; rx: {rx}")
        if cpu_cycle in [20, 60, 100, 140, 180, 220]:
            total_signal_strength += rx * cpu_cycle

        cpu_cycle += 1

    if instruction == "addx":
        rx += int(parts[1])

print(total_signal_strength)