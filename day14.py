import sys
from dataclasses import dataclass

AIR = "."
ROCK = "#"
SOURCE = "+"
SAND = "o"


@dataclass
class Pos:
    x: int
    y: int


def print_grid(grid: list[list[str]], x_offset: int):
    print()
    max_x = len(grid[0])
    header_lines = len(str(max_x + x_offset))
    for i in range(header_lines):
        print("  ", end="")
        for x in range(x_offset, max_x + x_offset):
            if x % 5 == 0:
                print(str(x)[i], end="")
            else:
                print(" ", end="")
        print()

    for y in range(len(grid)):
        print(y, end=" ")
        for x in range(max_x):
            print(grid[y][x], end="")
        print()


min_x = 500
max_x = 500
max_y = 0
rocks: list[Pos] = []
while line := sys.stdin.readline():
    parts = line.split("->")
    last_pos: Pos
    for i, part in enumerate(parts):
        pos_parts = part.split(",")
        pos = Pos(int(pos_parts[0]), int(pos_parts[1]))

        if i > 0:
            if pos.x == last_pos.x:
                for y in range(min(pos.y, last_pos.y), max(pos.y, last_pos.y) + 1):
                    rocks.append(Pos(pos.x, y))
            else:
                for x in range(min(pos.x, last_pos.x), max(pos.x, last_pos.x) + 1):
                    rocks.append(Pos(x, pos.y))

        if pos.x > max_x:
            max_x = pos.x
        if pos.y > max_y:
            max_y = pos.y
        if pos.x < min_x:
            min_x = pos.x

        last_pos = pos

grid: list[list[str]] = []
for _ in range(max_y + 1):
    grid.append([AIR] * (max_x - min_x + 1))

for rock in rocks:
    grid[rock.y][rock.x - min_x] = ROCK

grid[0][500 - min_x] = SOURCE

print_grid(grid, min_x)

i = 0
while True:
    y = 0
    x = 500 - min_x

    while y + 1 < len(grid):
        if grid[y + 1][x] == AIR:
            y += 1
            continue
        if grid[y + 1][x - 1] == AIR:
            y += 1
            x -= 1
            continue
        if grid[y + 1][x + 1] == AIR:
            y += 1
            x += 1
            continue
        break
    if y + 1 == len(grid):
        break

    grid[y][x] = SAND
    i += 1

    print(i)

print_grid(grid, min_x)
print(i)
