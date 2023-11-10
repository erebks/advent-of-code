#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 10 part 1

import re
import pdb

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
lines = [ # Score = 26397
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
        return c

    print("Round: %d, levels: %s"%(i, levels))
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
                    return c
                else:
                    print("Level closed %c & %c"%(o,c))
            else:
                # ERROR?!
                print("Should not come here?! entry: %s"%entry)
                exit(0)

        i += 1
        print("Round: %d, levels: %s"%(i, levels))
    if (len(levels) != 0):
        print("Incomplete Line")
        return None
    else:
        print("Correct Line")
        return True

pointsConv = {
    ')': 3,
    ']':57,
    '}':1197,
    '>':25137,
    }

points = 0

for l in lines:
    l = re.sub("\n","",l)
    print()
    print("#########################")
    print("Line: %s"%l)
    c = checkLine(l)
    if c != None and c != True:
        points += pointsConv[c]


print("Answer: %d" %points)
