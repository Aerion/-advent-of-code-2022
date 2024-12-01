import sys

cpu_cycle = 1
rx = 1
crt_row = ""
while line := sys.stdin.readline():
    parts = line.strip().split(" ")
    instruction = parts[0]

    if instruction == "noop":
        cost = 1
    else:
        cost = 2

    for _ in range(cost):
        sprite_positions = list(range(max(rx - 1, 0), min(rx + 1, 40) + 1, 1))
        if ((cpu_cycle - 1) % 40) in sprite_positions:
            print("#", end="")
        else:
            print(".", end="")
        if cpu_cycle % 40 == 0:
            print()

        cpu_cycle += 1

    if instruction == "addx":
        rx += int(parts[1])
