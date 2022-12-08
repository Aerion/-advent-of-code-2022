from dataclasses import dataclass
import sys


@dataclass
class Tree:
    height: int
    max_from_top: int
    max_from_bottom: int
    max_from_left: int
    max_from_right: int
    visible: bool


arr: list[list[Tree]] = []


y = 0
while line := sys.stdin.readline():
    line = line.strip()
    arr.append([])

    for x, char in enumerate(line):
        arr[y].append(
            Tree(int(char), int(char), int(char), int(char), int(char), False)
        )

    y += 1

for y in range(len(arr)):
    arr[y][0].visible = True
    arr[y][len(arr[0]) - 1].visible = True
for x in range(len(arr[0])):
    arr[0][x].visible = True
    arr[len(arr) - 1][x].visible = True


# Those four loops can probably be grouped, but well
for x in range(1, len(arr[0])):
    for y in range(1, len(arr)):
        top_node = arr[y - 1][x]
        cur_node = arr[y][x]
        if top_node.max_from_top < cur_node.height:
            cur_node.max_from_top = cur_node.height
            if not cur_node.visible:
                cur_node.visible = True
        else:
            cur_node.max_from_top = top_node.max_from_top

        bottom_node = arr[len(arr) - y][x]
        cur_node = arr[len(arr) - y - 1][x]
        if bottom_node.max_from_bottom < cur_node.height:
            cur_node.max_from_bottom = cur_node.height
            if not cur_node.visible:
                cur_node.visible = True
        else:
            cur_node.max_from_bottom = bottom_node.max_from_bottom


for y in range(1, len(arr)):
    for x in range(1, len(arr[y])):
        left_node = arr[y][x - 1]
        cur_node = arr[y][x]
        if left_node.max_from_left < cur_node.height:
            cur_node.max_from_left = cur_node.height
            if not cur_node.visible:
                cur_node.visible = True
        else:
            cur_node.max_from_left = left_node.max_from_left

        right_node = arr[y][len(arr[y]) - x]
        cur_node = arr[y][len(arr[y]) - x - 1]
        if right_node.max_from_right < cur_node.height:
            cur_node.max_from_right = cur_node.height
            if not cur_node.visible:
                cur_node.visible = True
        else:
            cur_node.max_from_right = right_node.max_from_right

total_visible_count = 0
for y in range(len(arr)):
    for x in range(len(arr[y])):
        if arr[y][x].visible:
            total_visible_count += 1
print(total_visible_count)