#!/usr/bin/env python

from aocd import puzzle, submit
from dataclasses import dataclass
from collections import defaultdict, deque
from datetime import timedelta
from enum import IntEnum, Enum
from functools import cache
from rich import print
from sys import stderr
from typing import Callable
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

class InstructionResult(Enum):
    NOTHING = 0
    HALTED = 1
    OUTPUT = 2

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

class Software:
    program: list[int]
    ip: int
    output: list[int]
    inputs: list[int]

    def __init__(self, program: list[int], inputs: list[int]):
        self.program = program[:]
        self.ip = 0
        self.output = []
        self.inputs = inputs
        self.input_idx = 0
    
    def _exec_instruction(self):
        op_code, parameters = parse_instruction(self.ip, self.program)

        if op_code == OpCode.HALT:
            # No need to process anymore if we must halt
            return InstructionResult.HALTED
        
        self.ip += 1 + len(parameters)

        if op_code == OpCode.ADD:
            output_address = parameters[2]
            self.program[output_address] = self.program[parameters[0]] + self.program[parameters[1]]
            return InstructionResult.NOTHING
        if op_code == OpCode.MULT:
            output_address = parameters[2]
            self.program[output_address] = self.program[parameters[0]] * self.program[parameters[1]]
            return InstructionResult.NOTHING
        if op_code == OpCode.WRITE_AT:
            self.program[parameters[0]] = self.inputs[self.input_idx]
            self.input_idx += 1
            return InstructionResult.NOTHING
        if op_code == OpCode.OUTPUT:
            self.output.append(self.program[parameters[0]])
            return InstructionResult.OUTPUT
        if op_code == OpCode.JNZ:
            if self.program[parameters[0]] != 0:
                self.ip = self.program[parameters[1]]
            return InstructionResult.NOTHING
        if op_code == OpCode.JZ:
            if self.program[parameters[0]] == 0:
                self.ip = self.program[parameters[1]]
            return InstructionResult.NOTHING
        if op_code == OpCode.JLT:
            self.program[parameters[2]] = 1 if self.program[parameters[0]] < self.program[parameters[1]] else 0
            return InstructionResult.NOTHING
        if op_code == OpCode.JEQ:
            self.program[parameters[2]] = 1 if self.program[parameters[0]] == self.program[parameters[1]] else 0
            return InstructionResult.NOTHING

        print(f"[bold red]Unexpected op_code {op_code}[/]")
        assert False

    def run_until_halt(self):
        while self._exec_instruction() != InstructionResult.HALTED:
            continue
    
    def run_until_output_or_halt(self):
        while True:
            instruction_result = self._exec_instruction()
            if instruction_result == InstructionResult.HALTED or instruction_result == InstructionResult.OUTPUT:
                return instruction_result

    def get_last_output(self):
        return self.output[-1]

def run_amplifiers(program: list[int], sequence: list[int]):
    return run_amplifiers_fbl(program, sequence)

def run_amplifiers_fbl(program: list[int], sequence: list[int]):
    inputs = [[phase] for phase in sequence]
    inputs[0].append(0)
    softwares: list[Software] = [Software(program, input) for input in inputs]

    instruction_result = False
    while instruction_result != InstructionResult.HALTED:
        for i, software in enumerate(softwares):
            instruction_result = software.run_until_output_or_halt()
            if instruction_result != InstructionResult.HALTED:
                inputs[(i + 1) % len(softwares)].append(software.get_last_output())

    return softwares[-1].get_last_output()

assert run_amplifiers([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0]) == 43210
assert run_amplifiers([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]) == 54321
assert run_amplifiers([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]) == 65210
assert run_amplifiers_fbl([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]) == 139629729
assert run_amplifiers_fbl([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6]) == 18216

program = [int(x) for x in data.split(",")]

result = 0
for a in range(5, 10):
    for b in range(5, 10):
        for c in range(5, 10):
            for d in range(5, 10):
                for e in range(5, 10):
                    if len(set((a,b,c,d,e))) != 5:
                        continue
                    signal = run_amplifiers_fbl(program, [a,b,c,d,e])
                    result = max(signal, result)

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)