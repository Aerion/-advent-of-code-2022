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
    JNZ = 5,
    JZ = 6
    JLT = 7
    JEQ = 8
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
    OpCode.JNZ: 2,
    OpCode.JZ: 2,
    OpCode.JLT: 3,
    OpCode.JEQ: 3,
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

def run_program(program: list[int], inputs: list[int]):
    ip = 0
    input_idx = 0
    output = []
    while True:
        op_code, parameters = parse_instruction(ip, program)

        if op_code == OpCode.HALT:
            # No need to process anymore if we must halt
            break
        
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
            program[parameters[0]] = inputs[input_idx]
            input_idx += 1
            continue
        if op_code == OpCode.OUTPUT:
            output.append(program[parameters[0]])
            continue
        if op_code == OpCode.JNZ:
            if program[parameters[0]] != 0:
                ip = program[parameters[1]]
            continue
        if op_code == OpCode.JZ:
            if program[parameters[0]] == 0:
                ip = program[parameters[1]]
            continue
        if op_code == OpCode.JLT:
            program[parameters[2]] = 1 if program[parameters[0]] < program[parameters[1]] else 0
            continue
        if op_code == OpCode.JEQ:
            program[parameters[2]] = 1 if program[parameters[0]] == program[parameters[1]] else 0
            continue

        print(f"[bold red]Unexpected op_code {op_code}[/]")
        assert False
    
    return output

def run_amplifiers(program: list[int], sequence: list[int]):
    signal = 0
    for phase in sequence:
        outputs = run_program(program, [phase, signal])
        signal = outputs[-1]
    return signal

assert run_amplifiers([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0]) == 43210
assert run_amplifiers([3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]) == 54321
assert run_amplifiers([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]) == 65210

program = [int(x) for x in data.split(",")]

result = 0
for a in range(5):
    for b in range(5):
        for c in range(5):
            for d in range(5):
                for e in range(5):
                    if len(set((a,b,c,d,e))) != 5:
                        continue
                    signal = run_amplifiers(program, [a,b,c,d,e])
                    result = max(signal, result)

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)