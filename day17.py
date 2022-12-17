from enum import Enum
from dataclasses import dataclass
import sys
from typing import Optional

CHAMBER_WIDTH = 7


@dataclass
class RockPart:
    x: int
    y: int


class ROCK_TYPE(Enum):
    HORIZONTAL_LINE = 0
    STAR = 1
    L = 2
    VERTICAL_LINE = 3
    SQUARE = 4


class Rock:
    parts: list[RockPart]

    def __init__(self, parts: list[RockPart]):
        self.parts = parts

    def _move(self, x: int, y: int, obstructed_blocks: set[tuple[int, int]]):
        if any(
            (
                part.x + x == CHAMBER_WIDTH
                or part.y + y == -1
                or part.x + x == -1
                or (part.x + x, part.y + y) in obstructed_blocks
                for part in self.parts
            )
        ):
            return False

        for part in self.parts:
            part.x += x
            part.y += y
        return True

    def move_right(self, obstructed_blocks: set[tuple[int, int]]):
        # print('Move right')
        return self._move(1, 0, obstructed_blocks)

    def move_left(self, obstructed_blocks: set[tuple[int, int]]):
        # print('Move left')
        return self._move(-1, 0, obstructed_blocks)

    def move_down(self, obstructed_blocks: set[tuple[int, int]]):
        # print('Move down')
        return self._move(0, -1, obstructed_blocks)


def create_rock_parts(rock_type: ROCK_TYPE, max_height: int):
    if rock_type == ROCK_TYPE.HORIZONTAL_LINE:
        return [RockPart(x, max_height + 3) for x in range(2, 6)]
    if rock_type == ROCK_TYPE.STAR:
        return [RockPart(x, max_height + 4) for x in range(2, 5)] + [
            RockPart(3, max_height + 5),
            RockPart(3, max_height + 3),
        ]
    if rock_type == ROCK_TYPE.L:
        return [RockPart(x, max_height + 3) for x in range(2, 5)] + [
            RockPart(4, y) for y in range(max_height + 4, max_height + 6)
        ]
    if rock_type == ROCK_TYPE.VERTICAL_LINE:
        return [RockPart(2, y) for y in range(max_height + 3, max_height + 7)]
    if rock_type == ROCK_TYPE.SQUARE:
        return [
            RockPart(2, max_height + 3),
            RockPart(2, max_height + 4),
            RockPart(3, max_height + 3),
            RockPart(3, max_height + 4),
        ]
    raise Exception("unknown rock type " + str(rock_type))


ROCK_TYPES = [t for t in ROCK_TYPE]


def create_rock(rock_count: int, max_height: int):
    rock_parts = create_rock_parts(ROCK_TYPES[rock_count % len(ROCK_TYPES)], max_height)
    return Rock(rock_parts)


def print_grid(
    obstructed_blocks: set[tuple[int, int]],
    max_height: int,
    tmp_rock: Optional[Rock] = None,
):
    rock_parts = set((part.x, part.y) for part in tmp_rock.parts) if tmp_rock else []

    for y in range(max_height + 6, -1, -1):
        print("|", end="")
        for x in range(CHAMBER_WIDTH):
            if (x, y) in rock_parts:
                print("@", end="")
            else:
                print("#" if (x, y) in obstructed_blocks else ".", end="")
        print("|")
    for x in range(CHAMBER_WIDTH + 2):
        print("-", end="")
    print()


jet_pattern = sys.stdin.readline().strip()
jet_pattern_idx = 0


obstructed_blocks: set[tuple[int, int]] = set()
max_height = -1
for i in range(2022):
    rock = create_rock(i, max_height +1)
    # print_grid(obstructed_blocks, max_height, rock)

    while True:
        jet_direction = jet_pattern[jet_pattern_idx]
        jet_pattern_idx += 1
        if jet_pattern_idx == len(jet_pattern):
            jet_pattern_idx = 0

        if jet_direction == ">":
            rock.move_right(obstructed_blocks)
        elif jet_direction == "<":
            rock.move_left(obstructed_blocks)

        # print_grid(obstructed_blocks, max_height, rock)

        if not rock.move_down(obstructed_blocks):
            break

        # print_grid(obstructed_blocks, max_height, rock)
    # print_grid(obstructed_blocks, max_height, rock)

    highest_rock_part = None
    for part in rock.parts:
        if part.y > max_height:
            max_height = part.y
        obstructed_blocks.add((part.x, part.y))

    rock_height = max((part.y for part in rock.parts))
    max_height = max(max_height, rock_height)

print(max_height + 1)
