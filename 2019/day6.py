#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import timedelta
from functools import cache
from rich import print
from sys import stderr
from typing import Optional
import time

EXAMPLE_IDX = None
_start_time = time.time()

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    # Override data if needed
    # data = """REPLACE_ME"""
    pass

print(f"Puzzle #{puzzle.day}", file=stderr)

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data", file=stderr)
else:
    print(f"Using PROD data", file=stderr)

#################################################################
# No changes before this line
#################################################################

@dataclass
class Node:
    name: str
    children: list = field(default_factory=list)
    height: Optional[int] = None

node_by_name: dict[str, Node] = {}

for line in data.splitlines():
    reference, orbiting = line.split(')')
    if reference not in node_by_name:
        node_by_name[reference] = Node(reference)
    if orbiting not in node_by_name:
        node_by_name[orbiting] = Node(orbiting)
    node_by_name[reference].children.append(node_by_name[orbiting])

def dfs_height(node: Node):
    for child in node.children:
        child.height = node.height + 1
        dfs_height(child)

root = node_by_name["COM"]
root.height = 0
dfs_height(root)

result = 0
for node in node_by_name.values():
    result += node.height

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if result is not None and EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)