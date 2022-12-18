from collections import defaultdict
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class Droplet:
    x: int
    y: int
    z: int


class Grid:
    droplets: dict[int, dict[int, dict[int, Droplet]]]

    def __init__(self):
        self.droplets = defaultdict(lambda: defaultdict(lambda: defaultdict(Droplet)))

    def add_droplet(self, x: int, y: int, z: int):
        droplets_z = self._get_droplets_z(x, y)
        droplets_z[z] = Droplet(x, y, z)

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
while line := sys.stdin.readline().rstrip():
    x, y, z = (int(part) for part in line.split(","))
    grid.add_droplet(x, y, z)

    for (addx, addy, addz) in [
        (0, 0, 1),
        (0, 0, -1),
        (0, 1, 0),
        (0, -1, 0),
        (-1, 0, 0),
        (1, 0, 0),
    ]:
        if grid.get_droplet(x + addx, y + addy, z + addz):
            adjacent_sides += 1
            working_side -= 1
        else:
            working_side += 1

print(adjacent_sides)
print(working_side)