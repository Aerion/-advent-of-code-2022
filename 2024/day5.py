#!/usr/bin/env python

from aocd import puzzle
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Self

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

@dataclass
class Node:
    value: int
    constraint_nodes_after: list[Self] = field(default_factory=list)

def are_pages_valid(pages: list[Node], nodes: dict[int, Node]):
    for i in range(1, len(pages)):
        page = pages[i]

        for j in range(i):
            before_page = pages[j]
            if before_page in page.constraint_nodes_after:
                return False
    
    return True

nodes: dict[int, Node] = {}

result = 0
read_constraints = True
for line in data.splitlines():
    if not line:
        # Middle of the input
        read_constraints = False
        continue
    
    if read_constraints:
        before_val, after_val = map(int, line.split('|'))
        if nodes.get(before_val) is None:
            nodes[before_val] = Node(before_val)
        if nodes.get(after_val) is None:
            nodes[after_val] = Node(after_val)
        nodes[before_val].constraint_nodes_after.append(nodes[after_val])
        continue

    pages = [nodes.get(int(x)) for x in line.split(',')]
    if are_pages_valid(pages, nodes):
        middle_page = pages[int(len(pages) / 2)].value
        print(middle_page)
        result += middle_page

print(f"Result: {result}")