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

#print(f"Puzzle #{puzzle.day}")

#if EXAMPLE_IDX is not None:
#    print(f"Using example #{EXAMPLE_IDX} data")
#else:
#    print(f"Using PROD data")

class Operation:
    left: str
    right: str
    operator: str
    output: str

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
    
    def __str__(self):
        return f"{self.left} {self.operator} {self.right} -> {self.output}"
    
    def __repr__(self):
        return self.__str__()

def get_door_values(prefix: str, values: dict[str, int]):
    interesting_doors = [(int(k[1:]), v) for k, v in values.items() if k[0] == prefix]
    interesting_doors.sort(reverse=True)
    result = (1 << (interesting_doors[0][0] + 1)) - 1
    for door in interesting_doors:
        if door[1] == 0:
            result ^= 1 << door[0]
    return result

def print_graph(operations: list[Operation]):
    print('graph R {')
    for i in range(1, 45):
        print(f"x{str(i).rjust(2, '0')} [shape=Mcircle]")
        print(f"y{str(i).rjust(2, '0')} [shape=Mcircle]")
    for i in range(1, 46):
        print(f"z{str(i).rjust(2, '0')} [shape=doublecircle fillcolor=yellow style=filled]")
    #print('graph [rankdir="LR"]')
    for operation in sorted(operations, key=lambda op: (op.operator, ''.join(sorted((op.left, op.right))))):
        op_node = f"{operation.left}_{operation.operator}_{operation.right}"
        for x in sorted((operation.left, operation.right)):
            print(x, " -- ", op_node)
        print(op_node, " -- ", operation.output)
        color = {"AND": "red", "XOR": "blue", "OR": "green"}[operation.operator]
        print(f"{op_node} [label={operation.operator} fillcolor={color} style=filled]")
    
    other_names = []
    for names in [(op.left, op.right, op.output) for op in operations]:
        for name in names:
            if not name[1:].isnumeric():
                print(f"{name} [shape=plain]")

    print("}")

s1, s2 = data.split("\n\n")
values = {}
for initial_line in s1.splitlines():
    left, right = initial_line.split(":")
    values[left] = int(right)

initial_x = get_door_values("x", values)
initial_y = get_door_values("y", values)
operations_to_execute: deque[Operation] = deque()
for operation_line in s2.splitlines():
    if operation_line == "y35 AND x35 -> z35":
        operation_line = "y35 AND x35 -> sgj"
    elif operation_line == "bbc XOR jkb -> sgj":
        operation_line = "bbc XOR jkb -> z35"
    elif operation_line == "tfw OR cgt -> z14":
        operation_line = "tfw OR cgt -> vss"
    elif operation_line == "nhg XOR ttd -> vss":
        operation_line = "nhg XOR ttd -> z14"
    elif operation_line == "nrr XOR sms -> kpp":
        operation_line = "nrr XOR sms -> z31"
    elif operation_line == "nrr AND sms -> z31":
        operation_line = "nrr AND sms -> kpp"
    elif operation_line == "y22 AND x22 -> kdh":
        operation_line = "y22 AND x22 -> hjf"
    elif operation_line == "y22 XOR x22 -> hjf":
        operation_line = "y22 XOR x22 -> kdh"
    left, operator, right, _, output = operation_line.split(" ")
    operation = Operation(left, right, operator, output)
    
    operations_to_execute.append(operation)

result = ",".join(sorted(("z35", "sgj", "z14", "vss", "kpp", "z31", "kdh", "hjf")))
print(result)
#print_graph(operations_to_execute)
#exit(0)

# x02 AND y02 -> carry
# x02 XOR y02 -> sum
sums_by_idx: dict[int, str] = {}
carries_by_idx: dict[int, str] = {}
for operation in operations_to_execute:
    if not (operation.left[0], operation.right[0]) in [("x", "y"), ("y", "x")]:
        continue
    idx = int(operation.left[1:])
    if operation.operator == "XOR":
        if idx in sums_by_idx:
            print(f"WARN: {idx} already in sums")
        if operation.output[0] == "z" and not (idx == 0 and operation.output == "z00"):
            print(f"WARN: sum output {idx} directly in {operation.output}")
        sums_by_idx[idx] = operation.output
    if operation.operator == "AND":
        if idx in carries_by_idx:
            print(f"WARN: {idx} already in carries")
        if operation.output[0] == "z":
            print(f"WARN: carry output {idx} directly in {operation.output}")
        carries_by_idx[idx] = operation.output


for operation in operations_to_execute:
    if operation.operator == "OR":
        if operation.output[0] == "z" and operation.output != "z45":
            print(f"WARN: OR output directly in {operation.output}")

for operation in operations_to_execute:
    if not operation.output[0] == "z":
        continue

    # Only check the z result nodes
    if operation.operator != "XOR":
        print(f"WARN: Non-XOR operation with output z for {operation}")
        continue

    parent_operations = sorted([op for op in operations_to_execute if op.output in [operation.left, operation.right]], key=lambda x: x.operator)
    if not parent_operations:
        print(f"WARN: No parent operations for {operation}")
        continue
    if parent_operations[0].operator != "OR" or parent_operations[1].operator != "XOR":
        print(f"WARN: Unexpected parent_operations for {operation}")
        print(parent_operations)
    

exit(0)
while operations_to_execute:
    operation = operations_to_execute.popleft()
    missing_operands = operation.get_missing_operands(values)
    if missing_operands:
        operations_to_execute.append(operation)
    else:
        operation.execute(values)
    

x_plus_y = get_door_values("z", values)
print(f"{initial_x} + {initial_y} = {x_plus_y} - {initial_x + initial_y == x_plus_y}")
print()

exit(0)
print(bin(result))
print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)