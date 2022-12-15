import sys
import re
from dataclasses import dataclass


@dataclass
class Pos:
    x: int
    y: int


NO_BEACON = "#"
BEACON = "B"
SENSOR = "S"
Y_TARGET = 2000000 # 10


y_line = {}  # holds only X positions
while line := sys.stdin.readline():
    match = re.match("Sensor at x=([^,]+), y=([^,]+):.+x=([^,]+), y=([^,]+)", line)
    sensor_pos = Pos(int(match.group(1)), int(match.group(2)))
    beacon_pos = Pos(int(match.group(3)), int(match.group(4)))
    print(f"{beacon_pos=}")

    if beacon_pos.y == Y_TARGET:
        y_line[beacon_pos.x] = BEACON
    if sensor_pos.y == Y_TARGET:
        y_line[sensor_pos.x] = SENSOR

    beacon_sensor_distance = abs(sensor_pos.x - beacon_pos.x) + abs(
        sensor_pos.y - beacon_pos.y
    )

    target_sensor_y_distance = abs(Y_TARGET - sensor_pos.y)
    if target_sensor_y_distance >= beacon_sensor_distance:
        continue

    # Our target line is affected by the current beacon
    x_count = beacon_sensor_distance - target_sensor_y_distance
    print(
        f"{sensor_pos=}; {beacon_pos=}; {beacon_sensor_distance=}; {target_sensor_y_distance=}; {x_count=}"
    )
    for x in range(sensor_pos.x - x_count, sensor_pos.x + x_count + 1, 1):
        if x not in y_line:
            y_line[x] = NO_BEACON


min_x = min(y_line.keys())
max_x = max(y_line.keys())
print(f"{min_x=}; {max_x=}")
no_beacon_count = 0

for x in range(min_x, max_x + 1, 1):
    item = y_line.get(x, ".")
    if item == NO_BEACON:
        no_beacon_count += 1
    # print(item, end="")
print()

print(f"{no_beacon_count=}")
