import sys
from dataclasses import dataclass


@dataclass
class Node:
    height: int
    visited: bool


@dataclass
class Position:
    x: int
    y: int


q = []
end_pos = Position(0, 0)

nodes: list[list[Node]] = []
y = 0
while line := sys.stdin.readline().strip():
    row = []
    for x, c in enumerate(line):
        if c == "S":
            c = "a"
        elif c == "E":
            end_pos = Position(x, y)
            c = "z"
        if c == "a":
            q.append((Position(x, y), 0))
        row.append(Node(ord(c) - ord("a"), False))
    nodes.append(row)
    y += 1

print(f"Target: {end_pos}")

while q:
    (pos, steps) = q.pop(0)
    if pos.y == end_pos.y and pos.x == end_pos.x:
        print(steps)
        break

    print(steps, pos)
    node = nodes[pos.y][pos.x]
    if node.visited:
        continue

    node.visited = True

    # Add neighbors
    def add_candidate(new_pos: Position):
        if (
            new_pos.y >= len(nodes)
            or new_pos.x >= len(nodes[0])
            or new_pos.y < 0
            or new_pos.x < 0
        ):
            return
        candidate = nodes[new_pos.y][new_pos.x]
        if candidate.visited or candidate.height > node.height + 1:
            return
        q.append((new_pos, steps + 1))

    add_candidate(Position(pos.x + 1, pos.y))
    add_candidate(Position(pos.x - 1, pos.y))
    add_candidate(Position(pos.x, pos.y + 1))
    add_candidate(Position(pos.x, pos.y - 1))
