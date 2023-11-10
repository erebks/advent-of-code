#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 12 part 1
import re
import pdb
import numpy as np
import copy

i = open("day15_in.txt", "r")
lines = i.readlines()
i.close()

# Can't use dijkstra as there are cycles and too many edges and vertices!


# Testinput -> 36 paths
lines = [
    "1163751742\n",
    "1381373672\n",
    "2136511328\n",
    "3694931569\n",
    "7463417111\n",
    "1319128137\n",
    "1359912421\n",
    "3125421639\n",
    "1293138521\n",
    "2311944581\n",
]

"""
lines = [
    "11111\n",
    "11111\n",
    "99999\n",
    "11111\n",
    "11111\n",
]
"""

field = []
for l in lines:
    l = re.sub("\n","",l)
    row = []
    for riskLevel in l:
        row.append(int(riskLevel))
    field.append(row)

field = np.array(field)

print(field)

def printField(field, pos):
    printField = np.array(field, 'U1')
    printField[pos] = '#'
#    print(printField)
    return printField

def stepForward(field, pos):
    nextStep = []
    # Get E if possible
    if (pos[1] == len(field[0])-1):
        E = None
    else:
        E = (pos[0], pos[1]+1)

    # Get S if possible
    if (pos[0] == len(field)-1):
        S = None
    else:
        S = (pos[0]+1, pos[1])

    if (S != None) and (E != None):
        if (field[S] < field[E]):
            nextStep.append(S)
        elif (field[S] > field[E]):
            nextStep.append(E)
        else:
            nextStep.append(S)
            nextStep.append(E)
    elif (S != None):
        nextStep.append(S)
    elif (E != None):
        nextStep.append(E)

    return nextStep

def stepBackward(field, pos):
    nextStep = []
    # Get N if possible
    if (pos[0] == 0):
        N = None
    else:
        N = (pos[0]-1, pos[1])

    # Get W if possible
    if (pos[1] == 0):
        W = None
    else:
        W = (pos[0], pos[1]-1)

    if (N != None) and (W != None):
        if (field[N] < field[W]):
            nextStep.append(N)
        elif (field[N] > field[W]):
            nextStep.append(W)
        else:
            nextStep.append(N)
            nextStep.append(W)
    elif (N != None):
        nextStep.append(N)
    elif (W != None):
        nextStep.append(W)

    return nextStep


def calcRiskOfPath(field, path):
    # calc risk of path excluding first and last element
#    print("path: {0}".format(path))
    totRisk = 0
    for pos in path[1:-1]:
        totRisk += field[pos]
#        print("pos: {2}, risk: {0}, totRisk: {1}".format(field[pos], totRisk, pos))

    return totRisk

def minRiskPath(field, backwardPath, path):
    backwardRisk = calcRiskOfPath(field, backwardPath)
    pathRisk = calcRiskOfPath(field, path)
#    print("\t\tminRiskPath: bP: {0} -> {1}, p: {2} -> {3}".format(backwardPath, backwardRisk, path, pathRisk))

    if (backwardRisk < pathRisk):
        return [backwardPath]
    elif (backwardRisk > pathRisk):
        return [path]
    else:
        return [backwardPath, path]

def replaceSubpath(path, subpath):
    # Find index of path which represents the start of subpath
    idx = path.index(subpath[0])
    path = path[:idx]
    for point in subpath:
        path.append(point)
    return path

def posAdjacentToPath(field, path, pos, forbiddenPos = None):
    # Check N if possible
    if not (pos[0] == 0):
        N = (pos[0]-1, pos[1])
        if (( N in path ) and (N != forbiddenPos)):
            return True, [N]

    # Check E if possible
    if not (pos[1] == len(field[0])-1):
        E = (pos[0], pos[1]+1)
        if (( E in path ) and ( E != forbiddenPos )):
            return True, [E]

    # Check S if possible
    if not (pos[0] == len(field)-1):
        S = (pos[0]+1, pos[1])
        if (( S in path ) and ( S != forbiddenPos )):
            return True, [S]

    # Get W if possible
    if not (pos[1] == 0):
        W = (pos[0], pos[1]-1)
        if (( W in path ) and ( W != forbiddenPos )):
            return True, [W]

    return False, []

def findBackwardPathUntilIntersection(field, forwardPath, backwardPath, foundPaths):
    adjacent = False
#    print("findBackwardPathUntilIntersection: b: {0}, f:{1}".format(backwardPath, foundPaths))
    while not adjacent:
        pos = backwardPath[-1]
        backward = stepBackward(field, pos)
        if backward == []:
#            print("\tStart found @{0}".format(pos))
            backwardPath.append(pos)
            foundPaths.append(backwardPath)
            return foundPaths
        elif len(backward) > 1:
#            print("\tbackward: {0}".format(backward))
            recurBackwardPath = copy.copy(backwardPath)
            recurBackwardPath.append(backward[1])
            recurFoundPath = findBackwardPathUntilIntersection(field,
                                                               forwardPath,
                                                               recurBackwardPath,
                                                               copy.copy(foundPaths)
                                                               )
#            print("\tRecur returned: {0}".format(recurFoundPath))
            for path in recurFoundPath:
                if path == []:
                    continue
                foundPaths.append(path)
            backwardPath.append(backward[0])
        else:
#            print("\tbackward: {0}".format(backward))
            backwardPath.append(backward[0])

        if (backward[0] in forwardPath):
#            print("\t{0} is on forwardPath".format(backward[0]))
            foundPaths.append(backwardPath)
            adjacent = True
        else:
            adjacent, nextStep = posAdjacentToPath(field, forwardPath, backward[0], forbiddenPos = backwardPath[0])
            if adjacent:
#                print("\t{0} is adjacent".format(backward[0]))
                backwardPath.append(nextStep[0])
                foundPaths.append(backwardPath)

    return foundPaths

def findForwardPathUntilEnd(field, forwardPath, foundPaths):
    obsolete = False
    print("findForwardPathUntilEnd: forw: {0}, found:{1}".format(forwardPath, foundPaths))

    while not obsolete:
        pos = forwardPath[-1]
        forward = stepForward(field, pos)
        if forward == []:
            print("\tEnd found!")
            forwardPath.append(pos)
            foundPaths.append(forwardPath)
            return foundPaths

        if len(forward) > 1:
            print("\tforward: {0}".format(forward))
            recurForwardPath = copy.copy(forwardPath)
            recurForwardPath.append(forward[1])
            recurFoundPaths = findForwardPathUntilEnd(field,
                                                      recurForwardPath,
                                                      copy.copy(foundPaths))

            print("\tRecur returned: {0}".format(recurFoundPaths))
            for path in recurFoundPaths:
                if path == []:
                    continue
                foundPaths.append(path)

            # Clean up
            res = []
            [res.append(x) for x in foundPaths if x not in res]
            foundPaths = res

            forwardPath.append(forward[0])

        else:
            print("\tforward: {0}".format(forward[0]))
            forwardPath.append(forward[0])

        # Check if backward paths return optimal
        backwardPaths = findBackwardPathUntilIntersection(field, forwardPath, [forwardPath[-1]], [])
        for backwardPath in backwardPaths:
            if backwardPath == []:
                print("\tNo backwardPath")
                continue
            elif len(backwardPath) == 2:
                print("\tIgnore backwardPath")
                # All is good - just took a step back
                continue
            else:
                # Check if backwardPath is actually better
                #   if yes -> rewrite forwardpath
                # Get intersection point
                revBackw = copy.deepcopy(backwardPath)
                revBackw.reverse()
                minRiskPaths = minRiskPath(field,
                                           revBackw,
                                           forwardPath[forwardPath.index(backwardPath[-1]):])
                if len(minRiskPaths) > 1:
                    print("\tPaths equally good")
                    continue
                elif not minRiskPaths[0] == []:
                    print("\tUsing path: {0}".format(minRiskPaths[0]))
                    forwardPath = replaceSubpath(forwardPath, minRiskPaths[0])
                    print("\tNewPath: {0}".format(forwardPath))


"""
forwardPath = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3), (4,3), (4,4), (4,5), (5,5), (6,5), (6,6), (7,6), (7,7), (7,8)]
found = findBackwardPathUntilIntersection(field, forwardPath, [forwardPath[-1]], [])
print("Found Paths: {0}".format(found))
breakpoint()
"""

optPath = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,6), (3,7), (4,7), (5,7), (5,8), (6,8), (7,8), (8,8), (8,9), (9,9), (9,9)]

found = findForwardPathUntilEnd(field, [(0,0)], [])
res = []
[res.append(x) for x in found if x not in res]

for path in res:
    risk = calcRiskOfPath(field, path)
    print("Path: {0} -> risk: {1}".format(path, risk))
