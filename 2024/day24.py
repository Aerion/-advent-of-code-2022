#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict, deque

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    # Override data if needed
    data = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

    data = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
    pass

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

class Operation:
    def __init__(self, left, right, operator, output):
        self.left = left
        self.right = right
        self.operator = operator
        self.output = output
    
    def get_missing_operands(self, available_values):
        result = []
        if self.left not in available_values:
            result.append(self.left)
        if self.right not in available_values:
            result.append(self.right)
        return result
    
    def execute(self, values):
        values[self.output] = self._get_result(values)
    
    def _get_result(self, values):
        left = values[self.left]
        right = values[self.right]

        if self.operator == "AND":
            return left & right
        if self.operator == "OR":
            return left | right
        if self.operator == "XOR":
            return left ^ right

        assert False

s1, s2 = data.split("\n\n")
values = {}
for initial_line in s1.splitlines():
    left, right = initial_line.split(":")
    values[left] = int(right)

operations_to_execute = deque()
for operation_line in s2.splitlines():
    left, operator, right, _, output = operation_line.split(" ")
    operation = Operation(left, right, operator, output)
    
    operations_to_execute.append(operation)

while operations_to_execute:
    operation = operations_to_execute.popleft()
    missing_operands = operation.get_missing_operands(values)
    if missing_operands:
        operations_to_execute.append(operation)
    else:
        operation.execute(values)
    

interesting_doors = [(int(k[1:]), v) for k, v in values.items() if k[0] == "z"]
interesting_doors.sort(reverse=True)
print(interesting_doors)
result = (1 << (interesting_doors[0][0] + 1)) - 1
print(bin(result))
for door in interesting_doors:
    if door[1] == 0:
        result ^= 1 << door[0]
print(bin(result))
print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)