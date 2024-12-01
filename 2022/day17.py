from enum import Enum
from dataclasses import dataclass
import sys
from typing import Optional
from tqdm import tqdm

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
    type: ROCK_TYPE

    def __init__(self, parts: list[RockPart], rock_type: ROCK_TYPE):
        self.parts = parts
        self.type = rock_type

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
    rock_type = ROCK_TYPES[rock_count % len(ROCK_TYPES)]
    rock_parts = create_rock_parts(rock_type, max_height)
    return Rock(rock_parts, rock_type)


def print_grid(
    obstructed_blocks: set[tuple[int, int]],
    max_height: int,
    tmp_rock: Optional[Rock] = None,
):

    return
    rock_parts = set((part.x, part.y) for part in tmp_rock.parts) if tmp_rock else []

    for y in range(max_height + 6, max_height - 10, -1):
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

cycle_detection_pattern: list[Rock] = []
cycle_detection_pattern_length = len(ROCK_TYPES) * 2
cycle_detection_pattern_evaluation_start = 10_000
cycle_detection_pattern_height_start = 0
cycle_detection_pattern_height = 0
cycle_detection_rocks_between_patterns = 0

cycle_detection_index = 0

NUMBER_OF_ROCKS = 1000000000000 # 2022 # 100_000 # 2022 # 1000000000000

obstructed_blocks: set[tuple[int, int]] = set()
max_height = -1
i = 0
skipped_rocks = 0
skipped_height = 0
a = 0
while i < NUMBER_OF_ROCKS:
    # print(i)
    rock = create_rock(i, max_height + 1)
    if skipped_rocks > 0:
        print_grid(obstructed_blocks, max_height, rock)

    while True:
        jet_direction = jet_pattern[jet_pattern_idx]
        jet_pattern_idx += 1
        if jet_pattern_idx == len(jet_pattern):
            jet_pattern_idx = 0

        if jet_direction == ">":
            rock.move_right(obstructed_blocks)
        elif jet_direction == "<":
            rock.move_left(obstructed_blocks)

        # if skipped_rocks > 0:
        #     print_grid(obstructed_blocks, max_height, rock)

        if not rock.move_down(obstructed_blocks):
            break

        # if skipped_rocks > 0:
        #     print_grid(obstructed_blocks, max_height, rock)
    if skipped_rocks > 0:
        print_grid(obstructed_blocks, max_height, rock)
        a += 1
        if a > 5:
            pass
            # exit(0)

    highest_rock_part = None
    for part in rock.parts:
        if part.y > max_height:
            max_height = part.y
        obstructed_blocks.add((part.x, part.y))

    rock_height = max((part.y for part in rock.parts))
    max_height = max(max_height, rock_height)

    i += 1

    if i <= cycle_detection_pattern_evaluation_start or skipped_rocks > 0:
        continue

    if len(cycle_detection_pattern) == 0:
        cycle_detection_pattern_height_start = max_height

    if len(cycle_detection_pattern) < cycle_detection_pattern_length:
        cycle_detection_pattern.append(rock)
    else:
        if (
            cycle_detection_pattern[cycle_detection_index].type == rock.type
            and cycle_detection_pattern[cycle_detection_index].parts[0].x == rock.parts[0].x
        ):
            cycle_detection_index += 1
        else:
            cycle_detection_index = 0

    if cycle_detection_index == cycle_detection_pattern_length:
        true_pattern_length = i - cycle_detection_pattern_evaluation_start
        cycle_detection_pattern_height = (
            max_height - cycle_detection_pattern_height_start
        )
        print(f"{i=} {cycle_detection_pattern_height=} {true_pattern_length=}")
        patterns_to_add = (NUMBER_OF_ROCKS - i) // (true_pattern_length)
        skipped_height = (patterns_to_add) * (cycle_detection_pattern_height)
        rocks_to_add = patterns_to_add * (true_pattern_length)

        print(f"Added {patterns_to_add} patterns for {rocks_to_add} rocks, skipping {skipped_height} height")

        cycle_detection_index = 0
        cycle_detection_pattern_height_start = max_height
        cycle_detection_pattern_evaluation_start = i

        # TODO: prendre deuxieme iteration
        if a == 0:
            a += 1
            continue

        i += rocks_to_add
        skipped_rocks = rocks_to_add


print(max_height + 1)
print(max_height + 1 + skipped_height)
