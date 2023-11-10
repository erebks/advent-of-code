#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day20_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '1\n',
    '2\n',
    '-3\n',
    '3\n',
    '-2\n',
    '0\n',
    '4\n',
]

class Node():
    def __init__(self, value, idxInit, p=None, n=None):
        self.value = value
        self.p = p
        self.n = n
        self.idxInit = idxInit

    def linkNext(self, n):
        self.n = n

    def linkPrev(self, p):
        self.p = p

    def next(self):
        return self.n

    def prev(self):
        return self.p

    def __repr__(self):
        return f"[Value: {self.value}, Next: {self.n.value}, Prev: {self.p.value}]"

    def __str__(self):
        return f"{self.value}"

def printAll(start):
    s = [start.value]
    node = start
    while True:
        node = node.next()
        if node == start:
            break
        s.append(node.value)

    print(s)

def mix(nodes):
    for i in range(len(nodes)):
        node = nodes[i]
        v = node.value

        if v == 0:
            continue
        elif v > 0:
            node.prev().linkNext(node.next())
            node.next().linkPrev(node.prev())

            n = node
            for i2 in range(v % (len(nodes)-1)):
                n = n.next()

            node.linkNext(n.next())
            n.next().linkPrev(node)

            node.linkPrev(n)
            n.linkNext(node)

        elif v < 0:
            node.prev().linkNext(node.next())
            node.next().linkPrev(node.prev())

            n = node
            v = abs(v) % (len(nodes)-1)
            for i2 in range((len(nodes)-1) - v):
                n = n.next()

            node.linkNext(n.next())
            n.next().linkPrev(node)

            node.linkPrev(n)
            n.linkNext(node)
    return nodes

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    i = 0
    node = Node(None, None)
    nodes = [node]
    idx_0 = None

    for l in lines:
        node = Node(int(re.sub('\n','',l)), i, p=nodes[-1])
        nodes.append(node)

        if int(re.sub('\n','',l)) == 0:
            print("0 Found!")
            idx_0 = i

        i += 1

    # Link head to tail
    nodes.pop(0)
    nodes[0].linkPrev(nodes[-1])
    nodes[-1].linkNext(nodes[0])

    # Fill the next entries
    for i in range(len(nodes)-1):
        nodes[i].linkNext(nodes[i+1])

    nodes = mix(nodes)

    print(nodes)
    printAll(nodes[0])

    i1k = 1000 % len(nodes)
    i2k = 2000 % len(nodes)
    i3k = 3000 % len(nodes)

    ans = 0

    n = nodes[idx_0]
    for i in range(i1k):
        n = n.next()
    ans += n.value

    n = nodes[idx_0]
    for i in range(i2k):
        n = n.next()
    ans += n.value

    n = nodes[idx_0]
    for i in range(i3k):
        n = n.next()
    ans += n.value

    print(f"Answer: {ans}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    i = 0
    node = Node(None, None)
    nodes = [node]
    idx_0 = None

    for l in lines:
        node = Node(int(re.sub('\n','',l)), i, p=nodes[-1])
        nodes.append(node)

        if int(re.sub('\n','',l)) == 0:
            print("0 Found!")
            idx_0 = i

        i += 1

    # Link head to tail
    nodes.pop(0)
    nodes[0].linkPrev(nodes[-1])
    nodes[-1].linkNext(nodes[0])

    # Fill the next entries
    for i in range(len(nodes)-1):
        nodes[i].linkNext(nodes[i+1])

    # Update with the "decryption key"
    for i in range(len(nodes)):
        nodes[i].value *= 811589153 #(811589153 % (len(nodes)-1))

    for i in range(10):
        nodes = mix(nodes)

    print(nodes)
    printAll(nodes[0])

    i1k = 1000 % len(nodes)
    i2k = 2000 % len(nodes)
    i3k = 3000 % len(nodes)

    ans = 0

    n = nodes[idx_0]
    for i in range(i1k):
        n = n.next()
    ans += n.value

    n = nodes[idx_0]
    for i in range(i2k):
        n = n.next()
    ans += n.value

    n = nodes[idx_0]
    for i in range(i3k):
        n = n.next()
    ans += n.value

    print(f"Answer: {ans}")


if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
