# importing modules
import pathlib
import feedparser
import helper
import random
import numpy as np
from random import sample

def create_sudoku_board():
    base = 3
    side = base * base

    def pattern(r, c): return (base * (r % base) + r // base + c) % side
    def shuffle(s): return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board

def board_to_markdown(board):
    markdown = "|---|---|---|---|---|---|---|---|---|\n"
    markdown += "|---|---|---|---|---|---|---|---|---|\n"
    for row in board:
        markdown += "|" + "|".join(f" {num} " if num != 0 else "   " for num in row) + "|\n"
    return markdown

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        board = create_sudoku_board()
        markdown_board = board_to_markdown(board)
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "sudoku_marker", markdown_board)
        f.open("w").write(c)
        print("Sudoku completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
