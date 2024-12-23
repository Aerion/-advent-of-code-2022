#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Node:
    name: str
    connected_names: set[str]

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    # Override data if needed
    pass

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

nodes_by_name: dict[str, Node] = {}

# TODO: do it with adj matrix?

for line in data.splitlines():
    left, right = line.split("-")
    if left not in nodes_by_name:
        nodes_by_name[left] = Node(left, set())
    if right not in nodes_by_name:
        nodes_by_name[right] = Node(right, set())

    nodes_by_name[left].connected_names.add(right)
    nodes_by_name[right].connected_names.add(left)

result = 0
matches = set()
for node_name, node in nodes_by_name.items():
    if node_name[0] == "t":
        for connected_name in node.connected_names:
            connected_node = nodes_by_name[connected_name]
            common_nodes = node.connected_names & connected_node.connected_names
            for common_node in common_nodes:
                matches.add(tuple(sorted((node_name, connected_name, common_node))))

result = len(matches)
print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)