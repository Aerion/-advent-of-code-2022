import sys
from dataclasses import dataclass
from typing import Callable

ROUND_COUNT = 20


def eval_operation(operation_text: str, old: int):
    return eval(operation_text) // 3


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    throw_to: Callable[[int], int]
    inspection_count = 0


monkeys: list[Monkey] = []
while line := sys.stdin.readline():
    starting_items = [
        int(item)
        for item in sys.stdin.readline().strip()[len("Starting items: ") :].split(",")
    ]
    operation_text = sys.stdin.readline().strip()[len("Operation: new =") :]
    divisible_by_test = int(sys.stdin.readline().strip().split(" ")[-1])
    if_true_monkey_idx = int(sys.stdin.readline().strip().split(" ")[-1])
    if_false_monkey_idx = int(sys.stdin.readline().strip().split(" ")[-1])
    sys.stdin.readline()

    operation = (lambda txt: lambda item: eval_operation(txt, item))(operation_text)
    throw_to = (lambda if_t, if_f, div: lambda item: if_t if item % div == 0 else if_f)(
        if_true_monkey_idx, if_false_monkey_idx, divisible_by_test
    )
    monkeys.append(Monkey(starting_items, operation, throw_to))

for _ in range(ROUND_COUNT):
    for monkey in monkeys:
        while monkey.items:
            monkey.inspection_count += 1
            item = monkey.items.pop(0)
            new_item = monkey.operation(item)
            new_monkey_idx = monkey.throw_to(new_item)
            monkeys[new_monkey_idx].items.append(new_item)

top_inspectors = (
    m.inspection_count
    for m in reversed(sorted(monkeys, key=lambda monkey: monkey.inspection_count))
)
print(next(top_inspectors) * next(top_inspectors))
