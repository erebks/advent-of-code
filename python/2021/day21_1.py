#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 21 part 1
import re
import pdb
import numpy as np
import copy

player1 = 6
player2 = 10

# Testinput -> P1 wins; P2 has 745 points; dice was rolled 993 times
#player1 = 4
#player2 = 8


class Dice:
    def __init__(self):
        self.rolled = 0

    def roll(self):
        roll = (self.rolled % 100) + 1
        self.rolled += 1
        return roll

class Field:
    def __init__(self, spaces):
        self.spaces = spaces # Number of spaces

    def move(self, pos, roll):
        if roll == 0:
            return pos
        else:
            return (((pos-1) + roll) % self.spaces) + 1

class Player:
    def __init__(self, startPos, dice, field):
        self.pos = startPos
        self.dice = dice
        self.field = field
        self.score = 0

    def play(self):
        # get dice score
        roll = 0
        roll += dice.roll()
        roll += dice.roll()
        roll += dice.roll()
        # Move forward
        self.pos = self.field.move(self.pos, roll)
        # Calc score
        self.score += self.pos
        return self.score

dice = Dice()
field = Field(10)

p1 = Player(player1, dice, field)
p2 = Player(player2, dice, field)

while True:
    if (p1.play() >= 1000):
        break
    if (p2.play() >= 1000):
        break

print("Game ended!")
print("Player1: {0}".format(p1.score))
print("Player2: {0}".format(p2.score))
print("Dice rolled: {0}".format(dice.rolled))

if p1.score < p2.score:
    ans = dice.rolled * p1.score
else:
    ans = dice.rolled * p2.score

print("Answer: {0}".format(ans))

"""
# Test input assert
assert p1.score == 1000
assert p2.score == 745
assert p2.score * dice.rolled == 739785
"""
