from collections import defaultdict
import sys
from dataclasses import dataclass
from typing import Optional

sys.setrecursionlimit(10_000_000)


@dataclass
class Droplet:
    x: int
    y: int
    z: int

all_droplets: list[Droplet] = []


class Grid:
    droplets: dict[int, dict[int, dict[int, Droplet]]]

    def __init__(self):
        self.droplets = defaultdict(lambda: defaultdict(lambda: defaultdict(Droplet)))

    def add_droplet(self, x: int, y: int, z: int):
        droplets_z = self._get_droplets_z(x, y)
        droplets_z[z] = Droplet(x, y, z)
        all_droplets.append(droplets_z[z])

    def get_droplet(self, x: int, y: int, z: int):
        droplets_z = self._get_droplets_z(x, y)
        return droplets_z.get(z)

    def _get_droplets_z(self, x: int, y: int):
        droplets_yz = self.droplets[x]
        if droplets_yz == None:
            return None
        droplets_z = droplets_yz[y]
        return droplets_z


grid = Grid()

adjacent_sides = 0
working_side = 0
min_z = None
max_z = None
min_x = None
max_x = None
min_y = None
max_y = None
while line := sys.stdin.readline().rstrip():
    x, y, z = (int(part) for part in line.split(","))
    grid.add_droplet(x, y, z)
    min_z = min(z, min_z or z)
    max_z = max(z, max_z or z)
    min_y = min(y, min_z or y)
    min_x = min(x, min_x or x)
    max_y = max(y, max_y or y)
    max_x = max(x, max_x or x)

min_x -= 3
min_y -= 3
min_z -= 3
max_x += 3
max_y += 3
max_z += 3

edges_count = 0


def is_in_bounds(x: int, y: int, z: int):
    return (
        x >= min_x
        and y >= min_y
        and z >= min_z
        and x < max_x
        and y < max_y
        and z < max_z
    )


visited_nodes: set[tuple[int, int, int]] = set()


def dfs(x: int, y: int, z: int):
    # print(x, y, z)
    edges_count = 0

    visited_nodes.add((x, y, z))
    for (addx, addy, addz, side) in [
        (0, 0, 1, "ahead"),
        (0, 0, -1, "behind"),
        (0, 1, 0, "top"),
        (0, -1, 0, "bottom"),
        (-1, 0, 0, "left"),
        (1, 0, 0, "right"),
    ]:
        if (x + addx, y + addy, z + addz) in visited_nodes or not is_in_bounds(x, y, z):
            continue

        droplet = grid.get_droplet(x + addx, y + addy, z + addz)
        if droplet:
            edges_count += 1

        if not droplet:
            edges_count += dfs(x + addx, y + addy, z + addz)
            continue

    return edges_count


print(dfs(min_x, min_y, min_z))