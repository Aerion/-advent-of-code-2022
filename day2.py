from enum import Enum
import sys


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    LOSE = 1
    DRAW = 2
    WIN = 3


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


def get_wished_move(opponent_move: Move, wished_result: Result):
    if wished_result == Result.DRAW:
        return opponent_move
    if wished_result == Result.LOSE:
        return {
            Move.ROCK: Move.SCISSORS,
            Move.SCISSORS: Move.PAPER,
            Move.PAPER: Move.ROCK,
        }[opponent_move]
    return {
        Move.ROCK: Move.PAPER,
        Move.SCISSORS: Move.ROCK,
        Move.PAPER: Move.SCISSORS,
    }[opponent_move]


total_score = 0
while line := sys.stdin.readline():
    line = line.strip()

    opponent_move = {"A": Move.ROCK, "B": Move.PAPER, "C": Move.SCISSORS}[line[0]]
    wished_result = {"X": Result.LOSE, "Y": Result.DRAW, "Z": Result.WIN}[line[2]]

    self_move = get_wished_move(opponent_move, wished_result)

    total_score += self_move.value + get_winning_score(self_move, opponent_move)

print(total_score)
