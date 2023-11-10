#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 4 part 1 and 2

import numpy as np
import re

i = open("day4_in.txt", "r")
lines = i.readlines()
i.close()
mat = []

"""
# Test input -> Should yield board 3 with 4512
lines = [
    "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1\n"
    "\n",
    "22 13 17 11  0\n",
    " 8  2 23  4 24\n",
    "21  9 14 16  7\n",
    " 6 10  3 18  5\n",
    " 1 12 20 15 19\n",
    "\n",
    " 3 15  0  2 22\n",
    " 9 18 13 17  5\n",
    "19  8  7 25 23\n",
    "20 11 10 24  4\n",
    "14 21 16 12  6\n",
    "\n",
    "14 21 17 24  4\n",
    "10 16 15  9 19\n",
    "18  8 23 26 20\n",
    "22 11 13  6  5\n",
    " 2  0 12  3  7\n",
]
"""

# class of a board
class BingoBoard:
    def __init__(self, board):
        self.board = board #numpy array
        self.drawn = np.zeros((len(self.board), len(self.board[0])), dtype=bool) # Bool-matrix of drawn numbers
        self.win = False

    def __str__(self):
        return str(self.board)
    def __repr__(self):
        return str(self.board)

    def newNumber(self, value):
        # A new number was drawn -> check if number is on board and if board won
        tile = np.where(self.board == value)
        if np.size(tile) == 0:
            # Not found
            return self.win
        else:
            # Set number to drawn
            self.drawn[tile] = True
            # Check if row or colum is full
            if np.all(self.drawn[tile[0],:]):
                self.win = True
            elif np.all(self.drawn[:,tile[1]]):
                self.win = True
            return self.win

    def calcSum(self):
        return self.board.sum() - self.board[self.drawn].sum()

numbers_drawn = []
# Read numbers to draw
for num in re.split(r"\D", lines[0][:-2]):
    numbers_drawn.append(int(num))

print(numbers_drawn)

bingoboards = []

playfield = []
# Read boards
for l in lines[2:]:
    if l == "\n":
        # End of playfield building -> Create new bingoboard
        playfield = np.array(playfield)
        bingoboard = BingoBoard(playfield)
        playfield = []
        bingoboards.append(bingoboard)
    else:
        row = []
        s1 = re.sub("\n","", l)     # remove new line
        s2 = re.sub("^\s+", "", s1)  # remove any whitespaces at start
        s3 = re.sub("\s+", ",", s2) # use ',' for delimiters
        for num in re.split("\D", s3):
            row.append(int(num))
        playfield.append(row)

# End of playfield building -> Create new bingoboard
playfield = np.array(playfield)
bingoboard = BingoBoard(playfield)
bingoboards.append(bingoboard)

scores = []

for num in numbers_drawn:
    for bingoboard in bingoboards:
        if (bingoboard.win == False):
            # Only if board did not already win
            if (bingoboard.newNumber(num) == True):
                # Win -> Save score
                scores.append(bingoboard.calcSum() * num)

print(scores)
