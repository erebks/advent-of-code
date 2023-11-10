#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 12 part 2

import re
import pdb
import numpy as np
import copy

i = open("day12_in.txt", "r")
lines = i.readlines()
i.close()

"""
# Testinput -> 36 paths
lines = [
    "start-A\n",
    "start-b\n",
    "A-c\n",
    "A-b\n",
    "b-d\n",
    "A-end\n",
    "b-end\n",
]
"""
"""
# Testinput -> 103 paths
lines = [
    "dc-end\n",
    "HN-start\n",
    "start-kj\n",
    "dc-start\n",
    "dc-HN\n",
    "LN-dc\n",
    "HN-end\n",
    "kj-sa\n",
    "kj-HN\n",
    "kj-dc\n",
]
"""
"""
# Testinput -> 3509 paths
lines = [
    "fs-end\n",
    "he-DX\n",
    "fs-he\n",
    "start-DX\n",
    "pj-DX\n",
    "end-zg\n",
    "zg-sl\n",
    "zg-pj\n",
    "pj-he\n",
    "RW-he\n",
    "fs-DX\n",
    "pj-RW\n",
    "zg-RW\n",
    "start-pj\n",
    "he-WI\n",
    "zg-he\n",
    "pj-fs\n",
    "start-RW\n",
]
"""

class SmallCave:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.visited = False

    def __str__(self):
        n_str = ""
        for n in self.neighbors:
            n_str += "%s, "%(n.name)
        return "{%s -> [%s]}"%(self.name, n_str)

    def __repr__(self):
        return self.__str__()

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def removeNeighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    def visit(self):
        if (self.visited == True):
            return False
        else:
            self.visited = True
            return True

    def resetVisit(self):
        self.visited = False

    def isDeadPath(self):
        # If only one smallcave neighbor
        if len(self.neighbors) == 1:
            if isinstance(self.neighbors[0], SmallCave):
                return True
        return False

class BigCave:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def __str__(self):
        n_str = ""
        for n in self.neighbors:
            n_str += "%s, "%(n.name)
        return "{%s -> [%s]}"%(self.name, n_str)

    def __repr__(self):
        return self.__str__()

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def removeNeighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    def visit(self):
        return True

    def resetVisit(self):
        return None

    def isDeadPath(self):
        # If only one smallcave neighbor
        if len(self.neighbors) == 1:
            if isinstance(self.neighbors[0], SmallCave):
                return True
        return False

class StartEndCave:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.visited = False

    def __str__(self):
        n_str = ""
        for n in self.neighbors:
            n_str += "%s, "%(n.name)
        return "{%s -> [%s]}"%(self.name, n_str)

    def __repr__(self):
        return self.__str__()

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def removeNeighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    def visit(self):
        if (self.visited == True):
            return False
        else:
            self.visited = True
            return True

    def resetVisit(self):
        self.visited = False

    def isDeadPath(self):
        return False

def getExistingCave(caves, name):
    for cave in caves:
        if cave.name == name:
            return cave
    return None

def addPath(caves, s, e):
    # Get new instance of s-cave
    s_cave = getExistingCave(caves, s)
    if (s_cave != None):
        print("Cave '%s' already exists" %s)
    else:
        print("Creating new cave '%s'" %s)
        if (s == 'start' or s == 'end'):
            s_cave = StartEndCave(s)
        elif (re.findall("[A-Z]", s)):
            s_cave = BigCave(s)
        else:
            s_cave = SmallCave(s)
        caves.append(s_cave)

    # Get new instance of e-cave
    e_cave = getExistingCave(caves, e)
    if (e_cave != None):
        print("Cave '%s' already exists" %e)
    else:
        print("Creating new cave '%s'" %e)
        if (e == 'start' or e == 'end'):
            e_cave = StartEndCave(e)
        elif (re.findall("[A-Z]", e)):
            e_cave = BigCave(e)
        else:
            e_cave = SmallCave(e)
        caves.append(e_cave)

    # Make them neighbors
    s_cave.addNeighbor(e_cave)
    e_cave.addNeighbor(s_cave)

    return caves

caves = []
for l in lines:
    l = re.sub("\n","",l)
    s, e = re.split("-", l)
    caves = addPath(caves, s, e)

# Check if there are any deadpaths and remove, rerun until no cave was removed
while True:
    break
    removed = False
    for cave in caves:
        if cave.isDeadPath():
            removed = True
            print("Removing cave '%s'"%cave.name)
            caves.remove(cave)
            neighbors = cave.neighbors
            for neighbor in neighbors:
                neighbor.removeNeighbor(cave)

    if removed == False:
        break

print(caves)

# Start with cave 'start' and go trough every neighbor
start_cave = None
end_cave = None
for cave in caves:
    if cave.name == 'start':
        start_cave = cave
        caves.remove(cave)
    elif cave.name == 'end':
        end_cave = cave
        caves.remove(cave)

if start_cave == None:
    print("Start cave not found")
    exit(0)

if end_cave == None:
    print("End cave not found")
    exit(0)

def findEnd(cave, caves_visited, caves_forbidden, caves_parent, end_cave):
    # Take a step and report possibilities
    caves_visited = copy.copy(caves_visited)
    caves_forbidden = copy.copy(caves_forbidden)
    if isinstance(cave, SmallCave):
        if len(caves_forbidden) > 1:
            # At start only start is there
            caves_forbidden.append(cave)
        else:
            if cave in caves_visited:
                for c in caves_visited:
                    caves_forbidden.append(c)
            else:
                caves_visited.append(cave)
    caves_parent = copy.copy(caves_parent)
    caves_parent.append(cave)
    paths = []
    for neighbor in cave.neighbors:
        print("@Cave %s -> found %s" %(cave.name, neighbor.name))
        if neighbor == end_cave:
            paths.append(copy.copy(caves_parent))
            paths[-1].append(end_cave)
            print("\tEnd cave found! Path: %s"%(printPath(paths[-1])))
        elif neighbor in caves_forbidden:
            print("\tAlready visited")
            continue
        else:
            print("\tSearching neighbors")
            path = findEnd(neighbor, caves_visited, caves_forbidden, caves_parent, end_cave)
            if not path == []:
                for p in path:
                    paths.append(p)
            else:
                print("\t\tSearch not succesfull!")
    return paths

def printPath(path):
    s = ""
    for cave in path:
        if cave.name == 'end':
            s += cave.name
        else:
            s += cave.name+" -> "
    return s

paths = []

for n in start_cave.neighbors:
    # Step through possibilities until end is reached
    caves_visited = [start_cave]
    caves_parent = [start_cave]
    pathsFound = findEnd(n, caves_visited, caves_visited, caves_parent, end_cave)
    for path in pathsFound:
        paths.append(path)

pathId = 1
for path in paths:
    print("ID %004d: %s"%(pathId,printPath(path)))
    pathId += 1
