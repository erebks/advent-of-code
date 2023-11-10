#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 10 part 2

import re
import pdb
import numpy as np

i = open("day10_in.txt", "r")
lines = i.readlines()
i.close()

# Testinput
"""
lines = [ # All valid
    "()\n",
    "[]\n",
    "<>\n",
    "{}\n",
    "([])\n",
    "{()()()}\n",
    "<([{}])>\n",
    "[<>({}){}[([])<>]]\n",
    "(((((((((())))))))))\n",
]
"""
"""
lines = [ # Corrupted
    "(]\n",
    "{()()()>\n",
    "(((()))}\n",
    "<([]){()}[{}])\n",
]
"""
"""
lines = [ # Score = 288957
    "[({(<(())[]>[[{[]{<()<>>\n", # incomplete
    "[(()[<>])]({[<{<<[]>>(\n", # incomplete
    "{([(<{}[<>[]}>{[]{[(<()>\n", # corrupted
    "(((({<>}<{<{<>}{[]{[]{}\n", # incomplete
    "[[<[([]))<([[{}[[()]]]\n", # corrupted
    "[{[{({}]{}}([{[{{{}}([]\n", # corrupted
    "{<[[]]>}<{[{[{[]{()[[[]\n", # incomplete
    "[<(<(<(<{}))><([]([]()\n", # corrupted
    "<{([([[(<>()){}]>(<<{{\n", # corrupted
    "<{([{{}}[<[[[<>{}]]]>[]\n", # incomplete
]
"""

# ([{<

def isOpeningBracket(c):
    if c == '(':
        return c
    elif c == '[':
        return c
    elif c == '{':
        return c
    elif c == '<':
        return c
    else:
        return False

def isClosingBracket(c):
    if c == ')':
        return c
    elif c == ']':
        return c
    elif c == '}':
        return c
    elif c == '>':
        return c
    else:
        return False

def bracketMatch(o,c):
    if o == '(' and c == ')':
        return True
    elif o == '[' and c == ']':
        return True
    elif o == '{' and c == '}':
        return True
    elif o == '<' and c == '>':
        return True

def checkLine(line):
    levels = []
    i = 0
    # first in line
    c = isOpeningBracket(line[0])
    if ( c != False):
        levels.append(c)
    else:
        # Corrupted! (or is it?)
        return c, levels

#    print("Round: %d, levels: %s"%(i, levels))
    for entry in line[1:]:
        c = isOpeningBracket(entry)
        if c != False:
            # Opening Bracket!
            levels.append(c)
        else:
            c = isClosingBracket(entry)
            if c != False:
                # Check if last level is closed
                o = levels.pop()
                if not bracketMatch(o,c):
                    print("Brackets %c and %c do not match"%(o,c))
                    return c, levels
            else:
                # ERROR?!
                print("Should not come here?! entry: %s"%entry)
                exit(0)

        i += 1
#        print("Round: %d, levels: %s"%(i, levels))
    if (len(levels) != 0):
        print("Incomplete Line")
        return None, levels
    else:
        print("Correct Line")
        return True, levels

bracketPairs = {
    '(':')',
    '[':']',
    '{':'}',
    '<':'>',
}

pointsConv = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def calcPoints(brackets):
    points = 0
    for bracket in brackets:
        points *= 5
        points += pointsConv[bracket]

    return points

points = []

for l in lines:
    l = re.sub("\n","",l)
    print()
    print("#########################")
    print("Line: %s"%l)
    c, levels = checkLine(l)
    if c == None:
        # Line incomplete -> close all levels
        closing = []
        for bracket in reversed(levels):
            closing.append(bracketPairs[bracket])
        print("Closing: %s"%closing)
        points.append(calcPoints(closing))

points = np.sort(np.array(points))

print("Points: %s" %points)
print("Anser: %s" %points[int(len(points)/2)])
