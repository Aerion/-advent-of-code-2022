import sys
import re
from dataclasses import dataclass
from tqdm import tqdm
import multiprocessing


@dataclass
class Pos:
    x: int
    y: int


NO_BEACON = "#"
BEACON = "B"
SENSOR = "S"
MAX_COORD = 4_000_000

impossible_ranges = {}


def add_impossible_range(y: int, start_x: int, end_x: int):
    if y not in impossible_ranges:
        impossible_ranges[y] = []

    impossible_ranges[y].append((start_x, end_x))


while line := sys.stdin.readline():
    match = re.match("Sensor at x=([^,]+), y=([^,]+):.+x=([^,]+), y=([^,]+)", line)
    sensor_pos = Pos(int(match.group(1)), int(match.group(2)))
    beacon_pos = Pos(int(match.group(3)), int(match.group(4)))
    print(f"{beacon_pos=}")

    if (
        beacon_pos.y >= 0
        and beacon_pos.y < MAX_COORD
        and beacon_pos.x >= 0
        and beacon_pos.x < MAX_COORD
    ):
        add_impossible_range(beacon_pos.y, beacon_pos.x, beacon_pos.x)
    if (
        sensor_pos.y >= 0
        and sensor_pos.y < MAX_COORD
        and sensor_pos.x >= 0
        and sensor_pos.x < MAX_COORD
    ):
        add_impossible_range(sensor_pos.y, sensor_pos.x, sensor_pos.x)

    for Y_TARGET in tqdm(range(MAX_COORD)):
        beacon_sensor_distance = abs(sensor_pos.x - beacon_pos.x) + abs(
            sensor_pos.y - beacon_pos.y
        )

        target_sensor_y_distance = abs(Y_TARGET - sensor_pos.y)
        if target_sensor_y_distance >= beacon_sensor_distance:
            continue

        # Our target line is affected by the current beacon
        x_count = beacon_sensor_distance - target_sensor_y_distance
        start_x = max(0, sensor_pos.x - x_count)
        end_x = min(sensor_pos.x + x_count, MAX_COORD)
        if end_x >= 0 and start_x < MAX_COORD:
            add_impossible_range(Y_TARGET, start_x, end_x)

print("Beacons parsed")


def parallel_finder(y):
    full_line = (1 << (MAX_COORD + 1)) - 1
    line = 0
    for r in impossible_ranges[y]:
        shifter = 1 << (r[1] - r[0] + 1)
        shifter -= 1
        shifter <<= r[0]
        line |= shifter

    if line != full_line:
        for x in range(MAX_COORD):
            if (1 << x) & line == 0:
                for _ in range(100):
                    print(f"FOUND!! {x=} {y=}")
                exit(0)

# There evidently is a faster solution than this bruteforce approach 🙃
start_coord = 0
total_coord = MAX_COORD - start_coord
with multiprocessing.Pool(16) as pool:
    r = list(tqdm(pool.imap(parallel_finder, range(start_coord, MAX_COORD)), total=total_coord))