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

def print_path(path: list[Node], msg: str, force=False):
    if False:
        print(f"{msg} {[x.value for x in path]}")

def print_dotformat(nodes: list[Node]):
    for node in nodes:
        for child in node.constraint_nodes_after:
            print(f"{node.value} -> {child.value}")

def find_valid_path(root: Node, end: Node, nodes_to_visit: list[Node], path: list[Node]):
    path.append(root)
    nodes_to_visit.remove(root)

    print_path(path, "Path")

    if root == end and not nodes_to_visit:
        # We won
        return path

    for child in root.constraint_nodes_after:
        is_valid = find_valid_path(child, end, nodes_to_visit, path)
        if is_valid:
            return is_valid
    
    # Not a correct path
    path.remove(root)
    nodes_to_visit.append(root)
    print_path(path, "Invalid path")
    return False

def are_pages_valid(pages: list[Node], nodes: dict[int, Node]):
    for i in range(1, len(pages)):
        page = pages[i]

        for j in range(i):
            before_page = pages[j]
            if before_page in page.constraint_nodes_after:
                #print("INVALID BECAUSE OF", page.value, before_page.value, [x.value for x in page.constraint_nodes_after])
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
    if not are_pages_valid(pages, nodes):
        new_nodes = { p.value: Node(p.value) for p in pages }
        
        end = None
        for page in pages:
            new_nodes[page.value].constraint_nodes_after = [new_nodes[x.value] for x in page.constraint_nodes_after if x.value in new_nodes]
            if len(new_nodes[page.value].constraint_nodes_after) == 0:
                if end is not None:
                    print("Two ends")
                    exit(42)
                end = new_nodes[page.value]

        start = None
        for new_node in new_nodes.values():
            found = False
            for other_node in new_nodes.values():
                if new_node in other_node.constraint_nodes_after:
                    found = True
            if not found:
                if start is not None:
                    print("Two starts")
                    exit(52)
                start = new_node
        
        #print(f"Start: {start.value}")
        #print(f"End: {end.value}")

        # print_dotformat(new_nodes.values())
        pages = find_valid_path(start, end, [n for n in new_nodes.values()], [])
        print_path(pages, "Path found", True)

        middle_page = pages[int(len(pages) / 2)].value
        print(middle_page)
        result += middle_page

print(f"Result: {result}")