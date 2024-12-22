#!/usr/bin/env python

from aocd import puzzle, submit
from collections import defaultdict

EXAMPLE_IDX = None

data = (puzzle.examples[EXAMPLE_IDX] if EXAMPLE_IDX is not None else puzzle).input_data
if EXAMPLE_IDX == 0:
    data = """123"""
    data = """1
2
3
2024"""

print(f"Puzzle #{puzzle.day}")

if EXAMPLE_IDX is not None:
    print(f"Using example #{EXAMPLE_IDX} data")
else:
    print(f"Using PROD data")

def get_secret(secret):
    first = ((secret * 64) ^ secret) % 16777216
    second = ((first // 32) ^ first) % 16777216
    third = ((second * 2048) ^ second) % 16777216
    secret = third
    return secret

def get_price(secret):
    return secret % 10

def get_total_price_by_sequence(sequence, price_by_sequence_list):
    result = 0
    for price_by_sequence in price_by_sequence_list:
        result += price_by_sequence.get(sequence, 0)
    return result

price_by_sequence_list: list[dict[tuple[int, int, int, int], int]] = []

PRICE_CHANGES = 2000

for line in data.splitlines():
    secret = int(line)

    prices = [get_price(secret)]
    prices_differences = [0]
    for i in range(PRICE_CHANGES):
        secret = get_secret(secret)
        prices.append(get_price(secret))
        prices_differences.append(prices[-1] - prices[-2])

    price_by_sequence = {}
    for i in range(4, len(prices)):
        sequence = tuple(prices_differences[i - 3: i + 1])
        if sequence in price_by_sequence:
            continue
        price_by_sequence[sequence] = prices[i]
    
    price_by_sequence_list.append(price_by_sequence)

result = 0

keys_to_evaluate = set()
for price_by_sequence in price_by_sequence_list:
    for key in price_by_sequence.keys():
        keys_to_evaluate.add(key)
for key in keys_to_evaluate:
    result = max(result, get_total_price_by_sequence(key, price_by_sequence_list))

print(f"Result: {result}")
if EXAMPLE_IDX is None and data == puzzle.input_data:
    submit(result)