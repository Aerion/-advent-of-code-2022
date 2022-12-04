import sys

total_common = 0
while line := sys.stdin.readline():
    line = line.strip()
    pairs = [
        list(range(int(x.split("-")[0]), int(x.split("-")[1]) + 1))
        for x in line.split(",")
    ]
    
    if set(pairs[0]).intersection(pairs[1]):
        total_common += 1

print(total_common)
