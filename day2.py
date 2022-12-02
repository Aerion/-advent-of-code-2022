from enum import Enum
import sys


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def get_winning_score(self_move: Move, opponent_move: Move):
    return {
        (Move.ROCK, Move.ROCK): 3,
        (Move.ROCK, Move.PAPER): 0,
        (Move.ROCK, Move.SCISSORS): 6,
        (Move.PAPER, Move.ROCK): 6,
        (Move.PAPER, Move.PAPER): 3,
        (Move.PAPER, Move.SCISSORS): 0,
        (Move.SCISSORS, Move.ROCK): 0,
        (Move.SCISSORS, Move.PAPER): 6,
        (Move.SCISSORS, Move.SCISSORS): 3,
    }[self_move, opponent_move]


total_score = 0
while line := sys.stdin.readline():
    line = line.strip()

    opponent_move = {"A": Move.ROCK, "B": Move.PAPER, "C": Move.SCISSORS}[line[0]]
    self_move = {"X": Move.ROCK, "Y": Move.PAPER, "Z": Move.SCISSORS}[line[2]]

    total_score += self_move.value + get_winning_score(self_move, opponent_move)

print(total_score)
