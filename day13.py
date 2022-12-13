import sys


def is_ordered(left, right):
    if type(left) == int and type(right) == int:
        if left == right:
            # Equal, unknown
            return None
        return left < right

    if type(left) == int:
        left = [left]
    elif type(right) == int:
        right = [right]

    # Both are lists now
    i = 0
    while i < len(left) and i < len(right):
        ordered = is_ordered(left[i], right[i])
        if ordered != None:
            return ordered
        # Equal, continue
        i += 1

    if i == len(left) and i == len(right):
        # Equal, unknown
        return None

    return i == len(left)


sum_ordered_indexes = 0
idx = 0
while line := sys.stdin.readline():
    idx += 1
    left = eval(line)
    right = eval(sys.stdin.readline())
    sys.stdin.readline()

    if is_ordered(left, right):
        sum_ordered_indexes += idx

print(sum_ordered_indexes)
