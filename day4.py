import sys

total_common = 0
while line := sys.stdin.readline():
    line = line.strip()
    pairs = [[int(s) for s in x.split("-")] for x in line.split(",")]

    if (pairs[0][0] <= pairs[1][0] and pairs[0][1] >= pairs[1][1]) or (
        pairs[1][0] <= pairs[0][0] and pairs[1][1] >= pairs[0][1]
    ):
        total_common += 1
        continue

print(total_common)
