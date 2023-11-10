#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy
import json
from itertools import zip_longest

i = open("day13_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '[1,1,3,1,1]\n',
    '[1,1,5,1,1]\n',
    '\n',
    '[[1],[2,3,4]]\n',
    '[[1],4]\n',
    '\n',
    '[9]\n',
    '[[8,7,6]]\n',
    '\n',
    '[[4,4],4,4]\n',
    '[[4,4],4,4,4]\n',
    '\n',
    '[7,7,7,7]\n',
    '[7,7,7]\n',
    '\n',
    '[]\n',
    '[3]\n',
    '\n',
    '[[[]]]\n',
    '[[]]\n',
    '\n',
    '[1,[2,[3,[4,[5,6,7]]]],8,9]\n',
    '[1,[2,[3,[4,[5,6,0]]]],8,9]\n',
]

def checkMsg(left, right, depth=0):

    indent = ' '*depth
#    print(f"{indent}{left} vs {right}")

    for l, r in list(zip_longest(left,right)):
        # print(f"{indent} {l} vs {r}")
        if l is None:
            # print(f"{indent}  l ran out")
            return True

        if r is None:
            # print(f"{indent}  r ran out")
            return False

        if type(l) is int and type(r) is int:
            if l < r:
                # print(f"{indent}  l < r => True")
                return True
            elif l > r:
                # print(f"{indent}  l > r => False")
                return False
            else:
                # print(f"{indent}  l = r => Continue")
                continue

        if type(l) is int and type(r) is not int:
            # print(f"{indent}  Mixed Types converting l")
            l = [l]
            ret = checkMsg(l, r, depth+1)
            if ret != None:
                return ret

        if type(r) is int and type(l) is not int:
            # print(f"{indent}  Mixed Types converting r")
            r = [r]
            ret = checkMsg(l, r, depth+1)
            if ret is not None:
                return ret

        if type(l) is list and type(r) is list:
            # print(f"{indent}  List")
            ret = checkMsg(l, r, depth+1)
            if ret is not None:
                return ret


def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    com = []
    idx = 0

    while True:
        try:
            msg = []
            msg.append(json.loads(lines[idx][:-1]))
            idx += 1
            msg.append(json.loads(lines[idx][:-1]))
            idx += 1
            idx += 1
            com.append(msg)
        except:
            break

    correctMsgs = 0

    for msg in range(len(com)):
        # print(f"{com[msg][0]} vs {com[msg][1]}")

        if checkMsg(com[msg][0], com[msg][1]):
            # print(f"Pair {msg+1} is Correct")
            correctMsgs += msg+1
        # else:
        #     print(f"Pair {msg+1} is Incorrect")

    print(f"Answer: {correctMsgs}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    com = []
    idx = 0

    for l in lines:
        if l == '\n':
            continue
        com.append(json.loads(l))

    com.append([[6]])
    com.append([[2]])

    m = np.zeros((len(com), len(com)), bool)

    for ileft in range(len(m)):
        for iright in range(len(m)):
            if ileft == iright:
                continue
            m[ileft, iright] = checkMsg(com[ileft], com[iright])

    order = []

    # Bring first col to all 0
    for i in range(m.shape[1]):
        for col in range(i, m.shape[1]):
            if np.sum(m[:,col]) == i:
                order.append(col)
                a = np.array(m[:,col])
                m[:,col] = np.array(m[:,i])
                m[:,i] = a

                # Also swap row
                a = np.array(m[col,:])
                m[col,:] = np.array(m[i,:])
                m[i,:] = a

                # Swap com
                a = copy.deepcopy(com[col])
                com[col] = copy.deepcopy(com[i])
                com[i] = a

    i6 = 0
    i2 = 0
    for imsg in range(len(com)):
        if com[imsg] == [[6]]:
            i6 = imsg+1
        if com[imsg] == [[2]]:
            i2 = imsg+1

    print(f"Answer: {i6*i2}")


if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)


# test all with all/2 -> now can generate map
