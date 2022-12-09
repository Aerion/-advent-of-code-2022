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

head_pos = Position(0, 0)
tail_pos = Position(0, 0)

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

        if abs(head_pos.y - tail_pos.y) >= 2 or abs(head_pos.x - tail_pos.x) >= 2:
            move_x = tail_pos.y == head_pos.y
            move_y = tail_pos.x == head_pos.x
            if (not move_x) and (not move_y):
                move_x = True
                move_y = True

            if move_x:
                if tail_pos.x > head_pos.x:
                    # Tail is at the right of the head
                    tail_pos.x -= 1
                else:
                    tail_pos.x += 1
            if move_y:
                if tail_pos.y > head_pos.y:
                    # Tail is at the top of the head
                    tail_pos.y -= 1
                else:
                    tail_pos.y += 1

        visited_positions.add(dataclasses.replace(tail_pos))


print(len(visited_positions))