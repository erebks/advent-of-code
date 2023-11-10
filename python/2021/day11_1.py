#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 11 part 1

import re
import pdb
import numpy as np

i = open("day11_in.txt", "r")
lines = i.readlines()
i.close()

"""
# Testinput -> 10 rounds 204 flashes; 100 rounds -> 1656 flashes
lines = [
    "5483143223\n",
    "2745854711\n",
    "5264556173\n",
    "6141336146\n",
    "6357385478\n",
    "4167524645\n",
    "2176841721\n",
    "6882881134\n",
    "4846848554\n",
    "5283751526\n",
]
"""

# NW |  N  | NE
# ---+-----+----
#  W |  X  | E
# ---+-----+----
# SW |  S  | SE

class Octopus:
    def __init__(self, posX, posY, energy_level):
        self.posX = posX
        self.posY = posY
        self.energy_level = energy_level
        self.flashed = False
        self.neighbors = {
            "N":  None,
            "NE": None,
            "E":  None,
            "SE": None,
            "S":  None,
            "SW": None,
            "W":  None,
            "NW": None
        }

    def __str__(self):
        try:
            N_str = "'N': (%d, %d), " %(self.neighbors['N'].posX, self.neighbors['N'].posY)
        except:
            N_str = ""

        try:
            NE_str = "'NE': (%d, %d), " %(self.neighbors['NE'].posX, self.neighbors['NE'].posY)
        except:
            NE_str = ""

        try:
            E_str = "'E': (%d, %d), " %(self.neighbors['E'].posX, self.neighbors['E'].posY)
        except:
            E_str = ""

        try:
            SE_str = "'SE': (%d, %d), " %(self.neighbors['SE'].posX, self.neighbors['SE'].posY)
        except:
            SE_str = ""

        try:
            S_str = "'S': (%d, %d), " %(self.neighbors['S'].posX, self.neighbors['S'].posY)
        except:
            S_str = ""

        try:
            SW_str = "'SW': (%d, %d), " %(self.neighbors['SW'].posX, self.neighbors['SW'].posY)
        except:
            SW_str = ""

        try:
            W_str = "'W': (%d, %d), " %(self.neighbors['W'].posX, self.neighbors['W'].posY)
        except:
            W_str = ""

        try:
            NW_str = "'NW': (%d, %d), " %(self.neighbors['NW'].posX, self.neighbors['NW'].posY)
        except:
            NW_str = ""

        neighbors_str = "{%s%s%s%s%s%s%s%s}" %(N_str, NE_str, E_str, SE_str, S_str, SW_str, W_str, NW_str)
        return "{Octopus @ (%d, %d), energy: %d, flashed: %s, neighbors: %s}" %(self.posX, self.posY, self.energy_level, self.flashed, neighbors_str)

    def __repr__(self):
        return self.__str__()

    def addNeighbors(self, neighbors):
        self.neighbors = neighbors

    def incEnergy(self):
        if (self.flashed == True):
            return False
        else:
            self.energy_level += 1
            if (self.energy_level > 9):
                print("Octopus @ (%d, %d) flashed!" %(self.posX, self.posY))
                self.energy_level = 0
                self.flashed = True
                flashed = 1
                for key, neighbor in self.neighbors.items():
                    try:
                        flashed += neighbor.incEnergy()
                    except AttributeError:
                        flashed += 0
                # Call neighbors?
                return flashed
            else:
                return False

    def resetFlash(self):
        self.flashed = False

# Convert string input to matrix

energyLevels = []

for l in lines:
    l = re.sub("\n","",l)
    row = []
    for c in l:
        row.append(int(c))
    energyLevels.append(row)

def mapEnergyLevelsToOctopusi(energyLevels):
    # Convert matrix to instances of octopusi
    octopusi = []
    for y in range(len(energyLevels)):
        octopusi_row = []
        for x in range(len(energyLevels[0])):
            octopus = Octopus(x,y,energyLevels[y][x])
            print("(%d, %d) -> %d -> %s"%(x,y, energyLevels[y][x], octopus))
            octopusi_row.append(octopus)
        octopusi.append(octopusi_row)

    return octopusi

def addNeighbors(octopusi):
    # Add neighbors to instances

    for y in range(len(octopusi)):
        for x in range(len(octopusi[0])):
            if (y == 0):
                N = None
            else:
                N = octopusi[y-1][x]

            if (y == 0 or x == (len(octopusi[0])-1)):
                NE = None
            else:
                NE = octopusi[y-1][x+1]

            if (x == (len(octopusi[0])-1)):
                E = None
            else:
                E = octopusi[y][x+1]

            if (y == (len(octopusi)-1) or x == (len(octopusi[0])-1)):
                SE = None
            else:
                SE = octopusi[y+1][x+1]

            if (y == len(octopusi)-1):
                S = None
            else:
                S = octopusi[y+1][x]

            if (y == (len(octopusi)-1) or x == 0):
                SW = None
            else:
                SW = octopusi[y+1][x-1]

            if (x == 0):
                W = None
            else:
                W = octopusi[y][x-1]

            if (y == 0 or x == 0):
                NW = None
            else:
                NW = octopusi[y-1][x-1]

            neighbors = {
                "N"  : N,
                "NE" : NE,
                "E"  : E,
                "SE" : SE,
                "S"  : S,
                "SW" : SW,
                "W"  : W,
                "NW" : NW
            }

            octopusi[y][x].addNeighbors(neighbors)

def printEnergyLevels(octopusi):
    energyLevels = []
    # Iterate over all octopusi and increse energy
    for octopusi_row in octopusi:
        row = []
        for octopus in octopusi_row:
            row.append(octopus.energy_level)
        energyLevels.append(row)

    print(energyLevels)

# Init for 100 rounds

octopusi = mapEnergyLevelsToOctopusi(energyLevels)
print(octopusi)
addNeighbors(octopusi)

print(octopusi)

flashes = 0
for i in range(100):
    accu = 0
    # Iterate over all octopusi and increse energy
    for octopusi_row in octopusi:
        for octopus in octopusi_row:
            accu += octopus.incEnergy()

    # Iterate over all octopusi and reset flashed
    for octopusi_row in octopusi:
        for octopus in octopusi_row:
            octopus.resetFlash()

    print("Round: %d -> flashes: %d"%(i+1, accu))
    flashes += accu
#    printEnergyLevels(octopusi)

print("Total flashes: %d" %flashes)
