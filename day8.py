from dataclasses import dataclass
import sys


arr: list[list[int]] = []


y = 0
while line := sys.stdin.readline():
    line = line.strip()
    arr.append([])

    for x, char in enumerate(line):
        arr[y].append(int(char))

    y += 1

max_scenic_score = 0
for y in range(len(arr)):
    for x in range(len(arr[y])):
        cur_height = arr[y][x]

        visible_from_top = 0
        visible_from_bottom = 0
        visible_from_left = 0
        visible_from_right = 0

        top_y = y - 1
        while top_y >= 0:
            visible_from_top += 1
            if arr[top_y][x] >= cur_height:
                break
            top_y -= 1

        bottom_y = y + 1
        while bottom_y < len(arr):
            visible_from_bottom += 1
            if arr[bottom_y][x] >= cur_height:
                break
            bottom_y += 1

        left_x = x - 1
        while left_x >= 0:
            visible_from_left += 1
            if arr[y][left_x] >= cur_height:
                break
            left_x -= 1

        right_x = x + 1
        while right_x < len(arr[y]):
            visible_from_right += 1
            if arr[y][right_x] >= cur_height:
                break
            right_x += 1

        scenic_score = (
            visible_from_bottom
            * visible_from_left
            * visible_from_right
            * visible_from_top
        )
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

print(max_scenic_score)
