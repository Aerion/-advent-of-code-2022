#!/usr/bin/env python

from aocd import puzzle, submit
from dataclasses import dataclass
from collections import defaultdict, deque
from datetime import timedelta
from enum import IntEnum
from functools import cache
from rich import print
from sys import stderr
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
class OpCode(IntEnum):
    ADD = 1
    MULT = 2
    WRITE_AT = 3
    OUTPUT = 4
    HALT = 99

class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

parameters_count_by_op_code: dict[OpCode, int] = {
    OpCode.ADD: 3,
    OpCode.MULT: 3,
    OpCode.WRITE_AT: 1,
    OpCode.OUTPUT: 1,
    OpCode.HALT: 0,
}

def parse_instruction(ip: int, program: list[int]) -> tuple[OpCode, list[int]]:
    op_code_value = program[ip] % 100 # Last 2 digits
    op_code = OpCode(op_code_value)

    # Read parameters
    parameters: list[int] = []
    for i in range(parameters_count_by_op_code[op_code]):
        parameter_mode = ParameterMode((program[ip] // (10 ** (2 + i))) % 10)
        if parameter_mode == ParameterMode.IMMEDIATE:
            param_position = ip + i + 1
        elif parameter_mode == ParameterMode.POSITION:
            param_position = program[ip + i + 1]
        else:
            assert False # Unexepcted parameter mode
        parameters.append(param_position)

    return op_code, parameters
    
assert parse_instruction(0, [1002, 4, 3, 4, 33]) == (OpCode.MULT, [4, 2, 4])

result = None
program = [int(x) for x in data.split(",")]

ip = 0
output = []
while True:
    op_code, parameters = parse_instruction(ip, program)

    if op_code == OpCode.HALT:
        # No need to process anymore if we must halt
        break

    assert not output or output[-1] == 0 # Each output must be 0
    
    ip += 1 + len(parameters)

    if op_code == OpCode.ADD:
        output_address = parameters[2]
        program[output_address] = program[parameters[0]] + program[parameters[1]]
        continue
    if op_code == OpCode.MULT:
        output_address = parameters[2]
        program[output_address] = program[parameters[0]] * program[parameters[1]]
        continue
    if op_code == OpCode.WRITE_AT:
        input = 1
        program[parameters[0]] = input
        continue
    if op_code == OpCode.OUTPUT:
        output.append(program[parameters[0]])
        continue

    print(f"[bold red]Unexpected op_code {op_code}[/bold red]")
    assert False

result = output[-1]
#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)