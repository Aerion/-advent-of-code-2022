import dataclasses
import sys
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


visited_positions = set()

start_pos = Position(12, 6)
head_pos = dataclasses.replace(start_pos)
tail_positions = [dataclasses.replace(start_pos) for _ in range(9)]

while line := sys.stdin.readline():
    parts = line.split(" ")
    direction = parts[0]
    count = int(parts[1])

    for i in range(count):
        if direction == "U":
            head_pos.y += 1
        elif direction == "D":
            head_pos.y -= 1
        elif direction == "R":
            head_pos.x += 1
        elif direction == "L":
            head_pos.x -= 1

        for tail_idx, tail_pos in enumerate(tail_positions):
            relative_head_pos = (
                head_pos if tail_idx == 0 else tail_positions[tail_idx - 1]
            )

            if (
                abs(relative_head_pos.y - tail_pos.y) >= 2
                or abs(relative_head_pos.x - tail_pos.x) >= 2
            ):
                move_x = tail_pos.y == relative_head_pos.y
                move_y = tail_pos.x == relative_head_pos.x
                if (not move_x) and (not move_y):
                    move_x = True
                    move_y = True

                if move_x:
                    if tail_pos.x > relative_head_pos.x:
                        # Tail is at the right of the head
                        tail_pos.x -= 1
                    else:
                        tail_pos.x += 1
                if move_y:
                    if tail_pos.y > relative_head_pos.y:
                        # Tail is at the top of the head
                        tail_pos.y -= 1
                    else:
                        tail_pos.y += 1

        visited_positions.add(dataclasses.replace(tail_positions[-1]))

    print()
    for y in range(26, -1, -1):
        for x in range(26):
            if head_pos.x == x and head_pos.y == y:
                print("H", end="")
                continue
            found = False
            for idx in range(len(tail_positions)):
                if tail_positions[idx].x == x and tail_positions[idx].y == y:
                    print(idx + 1, end="")
                    found = True
                    break
            if not found:
                print(".", end="")
        print()


print(len(visited_positions))
