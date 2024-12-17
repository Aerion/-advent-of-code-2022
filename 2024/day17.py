#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

# #     If register C contains 9, the program 2,6 would set register B to 1.
# data = """Register A: 0
# Register B: 0
# Register C: 9

# Program: 2,6"""
# #   If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
# data = """Register A: 10
# Register B: 0
# Register C: 0

# Program: 5,0,5,1,5,4"""
# #    If register B contains 29, the program 1,7 would set register B to 26.
# data = """Register A: 0
# Register B: 29
# Register C: 0

# Program: 1,7"""
# #    If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
# data = """Register A: 0
# Register B: 2024
# Register C: 43690

# Program: 4,0"""
# #    If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
# data = """Register A: 2024
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0"""

registers = {}

s1, s2 = data.split("\n\n")
for line in s1.splitlines():
    elms = line.split(":")
    reg_name = elms[0].split(' ')[-1]
    reg_value = int(elms[1])
    registers[reg_name] = reg_value

def debug(str):
    if False:
        print(str)

debug(registers)

result = []
instructions = [int(x) for x in s2.split(" ")[1].split(",")]
debug(instructions)
ip = -1
while ip + 1 < len(instructions):
    def get_literal():
        global ip
        ip += 1
        return instructions[ip]
    def get_combo_operand():
        global ip
        ip += 1
        print(ip)
        if 0 <= instructions[ip] <= 3:
            return instructions[ip]
        return registers[{
            4: "A",
            5: "B",
            6: "C",
        }[instructions[ip]]]

    ip += 1
    opcode = instructions[ip]
    debug(f"{ip=} {opcode=}")
    if opcode == 0:
        registers["A"] = registers["A"] // (2 ** get_combo_operand())
        continue
    if opcode == 1:
        registers["B"] = registers["B"] ^ get_literal()
        continue
    if opcode == 2:
        registers["B"] = get_combo_operand() % 8
        continue
    if opcode == 3:
        if registers["A"] != 0:
            ip = get_literal() - 1
            debug(f"jumping to {ip}")
        else:
            get_literal() # discard it if no jump
        continue
    if opcode == 4:
        ip += 1 # read operand but ignore it
        registers["B"] = registers["B"] ^registers["C"]
        continue
    if opcode == 5:
        result.append(get_combo_operand() % 8)
        continue
    if opcode == 6:
        registers["B"] = registers["A"] // (2 ** get_combo_operand())
        continue
    if opcode == 7:
        registers["C"] = registers["A"] // (2 ** get_combo_operand())
        continue
    
    assert False

debug(registers)
result = ','.join((str(x) for x in result))
print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)