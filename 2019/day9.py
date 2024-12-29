#!/usr/bin/env python

from aocd import puzzle, submit
from dataclasses import dataclass
from collections import defaultdict, deque
from datetime import timedelta
from enum import IntEnum, Enum
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
    RELATIVE = 9
    HALT = 99

class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

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
    OpCode.RELATIVE: 1,
}

def parse_instruction(ip: int, program: dict[int, int], relative_base: int) -> tuple[OpCode, list[int]]:
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
        elif parameter_mode == ParameterMode.RELATIVE:
            param_position = program[ip + i + 1] + relative_base
        else:
            assert False # Unexepcted parameter mode
        parameters.append(param_position)

    return op_code, parameters

class Software:
    program: dict[int, int]
    ip: int = 0
    outputs: list[int]
    inputs: list[int]
    relative_base: int = 0
    input_idx: int = 0

    def __init__(self, program: list[int], inputs: list[int]):
        self.program = defaultdict(int)
        for i, v in enumerate(program):
            self.program[i] = v
        self.inputs = inputs
        self.outputs = []
    
    def _exec_instruction(self):
        op_code, parameters = parse_instruction(self.ip, self.program, self.relative_base)

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
            self.outputs.append(self.program[parameters[0]])
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
        if op_code == OpCode.RELATIVE:
            self.relative_base += self.program[parameters[0]]
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
        return self.outputs[-1]


def run_program(program: list[int], inputs: list[int]):
    software = Software(program, inputs)
    software.run_until_halt()
    return software.outputs


assert run_program([104,1125899906842624,99], []) == [1125899906842624]
print("OK")
assert len(str(run_program([1102,34915192,34915192,7,4,7,99,0], [])[-1])) == 16
print("OK")
assert run_program([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], []) == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
print("OK")

program = [int(x) for x in data.split(",")]
output = run_program(program, [1])

assert(len(output)) == 1
result = output[0]

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)