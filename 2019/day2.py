#!/usr/bin/env python

from aocd import puzzle, submit
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
    HALT = 99

program = [int(x) for x in data.split(",")]
program[1] = 12
program[2] = 2

ip = 0
while ip < len(program):
    op_code = OpCode(program[ip])
    if op_code == OpCode.HALT:
        break

    left_operand = program[program[ip + 1]]
    right_operand = program[program[ip + 2]]
    output_pos = program[ip + 3]

    ip += 4

    if op_code == OpCode.ADD:
        program[output_pos] = left_operand + right_operand
        continue
    if op_code == OpCode.MULT:
        program[output_pos] = left_operand * right_operand
        continue

    print(f"[bold red]Unexpected op_code {op_code}[/bold red]")
    assert False

result = program[0]

#################################################################
# No changes after this line
#################################################################

_end_time = time.time()
print(f"Result: {result} (in {timedelta(seconds=_end_time - _start_time)})", file=stderr)
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)