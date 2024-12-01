import sys
from functools import cmp_to_key


def compare(left, right):
    if type(left) == int and type(right) == int:
        if left == right:
            # Equal, unknown
            return 0
        return -1 if left < right else 1

    if type(left) == int:
        left = [left]
    elif type(right) == int:
        right = [right]

    # Both are lists now
    i = 0
    while i < len(left) and i < len(right):
        comparison = compare(left[i], right[i])
        if comparison != 0:
            return comparison
        # Equal, continue
        i += 1

    if i == len(left) and i == len(right):
        # Equal, unknown
        return 0

    return -1 if i == len(left) else 1


sum_ordered_indexes = 0

packets = []
while line := sys.stdin.readline():
    if line.strip():
        packets.append(eval(line))

MAGIC_PACKET_1 = [[2]]
MAGIC_PACKET_2 = [[6]]
packets.append(MAGIC_PACKET_1)
packets.append(MAGIC_PACKET_2)

packets.sort(key=cmp_to_key(compare))
print((packets.index(MAGIC_PACKET_1) + 1) * (packets.index(MAGIC_PACKET_2) + 1))