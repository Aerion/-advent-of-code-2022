import sys

input = sys.stdin.readline().strip()

MARKER_LENGTH = 14
last_seen_pos = [-MARKER_LENGTH] * 26

first_noncontinuous_pos = 0
for pos, char in enumerate(input):
    val = ord(char) - ord('a')

    last_pos = last_seen_pos[val]
    if pos - last_pos >= MARKER_LENGTH:
        if pos - first_noncontinuous_pos == MARKER_LENGTH:
            print(str(pos))
            break
    else:
        first_noncontinuous_pos = max(last_seen_pos[val] + 1, first_noncontinuous_pos)

    last_seen_pos[val] = pos
