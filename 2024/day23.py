#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict
from dataclasses import dataclass

#def print(*args):
#    return

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

def find_maximal_cliques(clique: set[str], candidates: set[str], ignored: set[str]):
    if len(clique) + len(candidates) < 13:
        # Optim?
        return []
    if not candidates:
        # No more candidates to visit, we explored every common vertex of the clique
        if not ignored:
            # Nothing was ignored, it's a maximal clique
            if len(clique) == 13:
                print("n".join(sorted(clique)))
                exit(0)
            return [tuple(clique)]

        return []
    
    cliques = []
    for candidate_name in candidates:
        # For each vertex adjacent to our node
        candidate = nodes_by_name[candidate_name]

        # Future candidates are the adjacent of this adjacent node that are also part of the potential clique we're building.
        # Indeed, the current candidates are the ones common for each vertex visited so far in the clique
        future_candidates = candidate.connected_names & candidates

        # Future ignored are the connected ones that are also part of the ignored ones so far
        future_ignored = candidate.connected_names & ignored

        # Add the candidate to the clique
        clique.add(candidate_name)
        cliques.extend(find_maximal_cliques(clique, future_candidates, future_ignored))
        # Backtrack
        clique.remove(candidate_name)
    
    return cliques

maximal_cliques = find_maximal_cliques(set(), set(nodes_by_name.keys()), set())
maximum_clique = sorted(maximal_cliques, reverse=True, key=len)[0]
result = ",".join(sorted(x for x in maximum_clique))
print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)