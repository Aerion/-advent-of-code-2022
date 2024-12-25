#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict
from functools import cache

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    data = """029A
980A
179A
456A
379A"""

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

numpad = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
}

dirpad = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}

vector_by_numpad_dir = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1),
}

@cache
def get_numpad_sequences_for_button(start, target):
    return pad_dfs(numpad[start], numpad[target], [], 3, 4, (0, 3))

@cache
def get_dirpad_sequences_for_button(start, target):
    return pad_dfs(dirpad[start], dirpad[target], [], 3, 2, (0, 0))

def debug(str):
    #return
    print(str)

def pad_dfs(start_pos: tuple[int, int], end_pos: tuple[int, int], path: list[str], width: int, height: int, forbidden_gap: tuple[int, int]):
    if start_pos == end_pos:
        # Won
        return [path + ["A"]]

    possibilities = []
    if start_pos[0] < end_pos[0]:
        possibilities.append('>')
    if start_pos[1] < end_pos[1]:
        possibilities.append('v')
    if start_pos[1] > end_pos[1]:
        possibilities.append('^')
    if start_pos[0] > end_pos[0]:
        possibilities.append('<')
    
    result = []
    for possibility in possibilities:
        x_inc, y_inc = vector_by_numpad_dir[possibility]
        new_x, new_y = start_pos[0] + x_inc, start_pos[1] + y_inc
        if (new_x, new_y) == forbidden_gap:
            continue
        if new_x < 0 or new_x > width - 1 or new_y < 0 or new_y > height - 1:
            assert False # If we end up there, the possibilities were badly computed

        path.append(possibility)
        for valid_path in pad_dfs((new_x, new_y), end_pos, path, width, height, forbidden_gap):
            result.append(valid_path.copy())
        path.pop()
    
    return result

def get_pad_sequences_for_line_idx(idx, input, output, is_numpad):
    if idx == len(input):
        return [output]

    pad_target = input[idx]
    start = 'A' if idx == 0 else input[idx - 1]
    
    pad_function = get_numpad_sequences_for_button if is_numpad else get_dirpad_sequences_for_button
    pad_sequences = pad_function(start, pad_target)

    result = []
    for sequence in pad_sequences:
        for leaf_output in get_pad_sequences_for_line_idx(idx + 1, input, output + sequence, is_numpad):
            result.append(leaf_output.copy())
    
    return result

def get_numpad_sequences(line):
    return _get_pad_sequences_for_full_line(line, True)

@cache
def _get_pad_sequences_for_full_line(line, is_numpad):
    sequences = ["".join(x) for x in get_pad_sequences_for_line_idx(0, line, [], is_numpad)]
    return sequences

def split_sequence_into_subsequences_count(dirpad_sequence: str):
    sub_sequences_count = defaultdict(int)
    for sub_sequence in dirpad_sequence.split("A")[:-1]:
        sub_sequences_count[sub_sequence + "A"] += 1
    return sub_sequences_count

def get_splitted_sub_sequences_for_line(line):
    result = []
    for sequence in _get_pad_sequences_for_full_line(line, False):
        # TODO: Maybe ignore if it's already present?
        result.append(split_sequence_into_subsequences_count(sequence))
    
    return result

def get_subsequence_count_length(sub_sequence_count):
    result = sum(len(k) * v for k, v in sub_sequence_count.items())
    return result

def get_str_from_subsequences_count(subsequences_count: dict[str, int]):
    return "".join(k * v for k, v in subsequences_count.items())

def get_result_from_input(input: str, runs):
    min_length = 2**64
    numpad_sequences = get_numpad_sequences(input)
    for idx, numpad_sequence in enumerate(numpad_sequences):
        print(f"\tProcessing {numpad_sequence} ({idx+1}/{len(numpad_sequences)}) ", end="")
        length = get_shortest_chunk_length(numpad_sequence, runs)
        print(f"{length=}")
        if length < min_length:
            min_length = length
    
    numeric = int(input[:-1])
    result = numeric * min_length
    tuple_res = (result, min_length, numeric)
    return tuple_res

@cache
def get_shortest_chunk_length(chunk, level):
    if level == 0:
        return len(chunk)
    total_length = 0
    for sub_sequence, count in split_sequence_into_subsequences_count(chunk).items():
        min_length = 2**64
        for sequence_candidate in _get_pad_sequences_for_full_line(sub_sequence, False):
            length = get_shortest_chunk_length(sequence_candidate, level - 1) * count
            if length < min_length:
                min_length = length
        total_length += min_length
    return total_length

# Assertions
def run_assertions():
    def assert_equivalent(a, b):
        assert len(a) == len(b) and sorted(a) == sorted(b)
    def assert_dicts(a, b):
        assert len(a) == len(b)
        for key in a.keys():
            assert a.get(key) == b.get(key)
    def assert_strings(actual, expected):
        if actual != expected:
            print(f"Unexpected differences")
            print(f"\tExpected: {expected}")
            print(f"\tActual  : {actual}")
        assert actual == expected

    assert_equivalent(['<A^A>^^AvvvA', '<A^A^>^AvvvA', '<A^A^^>AvvvA'], get_numpad_sequences("029A"))

    subsequences_count = split_sequence_into_subsequences_count('<A^A>^^AvvvA')
    assert_dicts({'<A': 1, '^A': 1, '>^^A': 1, 'vvvA': 1}, subsequences_count)
    assert get_subsequence_count_length(subsequences_count) == len('<A^A>^^AvvvA')

    example_tests = {
        '029A': '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
        '980A': '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
        '179A': '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
        '456A': '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
        '379A': '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
    }
    example_outputs = {
        '029A': (68 * 29, 68, 29),
        '980A': (60 * 980, 60, 980),
        '179A': (68 * 179, 68, 179),
        '456A': (64 * 456, 64, 456),
        '379A': (64 * 379, 64, 379),
    }
    for example_input, example_expected in example_tests.items():
        print("Testing", example_input)
        
        actual = get_result_from_input(example_input, 2)
        print(f"\tExpecting: {example_outputs[example_input]}")
        print(f"\tActual   : {actual}")
        assert example_outputs[example_input] == actual
        assert example_outputs[example_input][1] == len(example_expected)
        
    print("Assertions passed")
run_assertions()

result = 0
for line in data.splitlines():
    line_result, min_length, numeric = get_result_from_input(line.strip(), 25)
    print(f"{line=} {line_result=} {min_length=} {numeric=}")
    result += line_result

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)