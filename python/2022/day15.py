#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day15_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16\n',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3\n',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16\n',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16\n',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16\n',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10\n',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10\n',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10\n',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17\n',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22\n',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3\n',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3\n',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3\n',
]

SENSOR = 1
BEACON = 2
SENSOR_RANGE = 3

def drawSensorField(field, sensor):
    distance = sensor['distance']
    i = 0
    i2 = 0
    updw = 0
    for y in range(sensor['pos'][1]-distance-1, sensor['pos'][1]+distance+1):

        if (i <= distance):
            updw = 0
        else:
            updw = 1

        if updw == 0:
            for x in range(sensor['pos'][0]-i2+1, sensor['pos'][0]+i2):
                field[y, x] = SENSOR_RANGE
            i2 += 1
        else:
            for x in range(sensor['pos'][0]-i2+1, sensor['pos'][0]+i2):
                field[y, x] = SENSOR_RANGE
            i2 -= 1
        i += 1


def printField(field):
    i = 0
    for row in range(len(field)):
        s = []
        for col in range(len(field[0])):
            if field[row, col] == 0:
                s.append('.')
            elif field[row, col] == SENSOR:
                s.append('S')
            elif field[row, col] == BEACON:
                s.append('B')
            elif field[row, col] == SENSOR_RANGE:
                s.append('#')
            else:
                print("problem!")
        print(''.join(s))

def printFieldOfInterest(field, yoi):
    for row in range(yoi-1, yoi+2):
        s = []
        for col in range(len(field[0])):
            if field[row, col] == 0:
                s.append('.')
            elif field[row, col] == SENSOR:
                s.append('S')
            elif field[row, col] == BEACON:
                s.append('B')
            elif field[row, col] == SENSOR_RANGE:
                s.append('#')
            else:
                print("problem!")
        print(''.join(s))


def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
        yoi = 10
    else:
        lines = i_lines
        yoi = 2000000

    sensors = []
    beacons = []

    spanX = [1000,0]
    spanY = [1000,0]

    for l in lines:
        l = re.sub('Sensor at ', '',l[:-1])
        l = re.sub('closest beacon is at ', '', l)
        l = re.sub('x=', '', l)
        l = re.sub('y=', '', l)
        l = re.sub(': ', ',', l)
        l = re.sub(', ', ',', l)
        sensor = {'pos': [0,0], 'link': [0,0], 'distance': 0}
        beacon = {'pos': [0,0], 'link': [0,0], 'distance': 0}

        sensor['pos'][0], sensor['pos'][1], beacon['pos'][0], beacon['pos'][1] = list(map(int, re.split(',', l)))

        distance = abs(beacon['pos'][0] - sensor['pos'][0]) + abs(beacon['pos'][1] - sensor['pos'][1])

        sensor['link'] = beacon['pos']
        sensor['distance'] = distance

        beacon['link'] = sensor['pos']
        beacon['distance'] = distance

        print(f"S@{sensor['pos']}, B@{beacon['pos']} with dist: {distance}")

        if (yoi <= sensor['pos'][1]+distance and yoi >= sensor['pos'][1]-distance):
            spanX[0] = min(spanX[0], sensor['pos'][0]-distance)
            spanY[0] = min(spanY[0], sensor['pos'][1]-distance)

            spanX[1] = max(spanX[1], sensor['pos'][0]+distance)
            spanY[1] = max(spanY[1], sensor['pos'][1]+distance)

            sensors.append(sensor)
            beacons.append(beacon)
            print("\t Of interest")
        else:
            print("\t Ignore")

    offsetX = -spanX[0]
    offsetY = -spanY[0]

    yoi += offsetY

    for sensor in sensors:
        sensor['pos'][0] += offsetX
        sensor['pos'][1] += offsetY

    for beacon in beacons:
        beacon['pos'][0] += offsetX
        beacon['pos'][1] += offsetY

    spanX = [spanX[0] + offsetX, spanX[1] + offsetX]
    spanY = [spanY[0] + offsetY, spanY[1] + offsetY]

    # Draw the field
    dimX = spanX[1]+1
    dimY = spanY[1]+1

    if dryRun:
        completeField = np.zeros([dimY, dimX], int)

    for sensor in sensors:
        print(sensor)
        distance = sensor['distance']
        field = np.zeros([distance*2 +1, distance*2 +1], int)

        s = copy.deepcopy(sensor)
        s['pos'][0] = distance
        s['pos'][1] = distance

        drawSensorField(field, s)

        pos = (s['pos'][1], s['pos'][0])
        field[pos] = SENSOR

        pos = (s['link'][1] - sensor['pos'][1] + distance, s['link'][0] - sensor['pos'][0] + distance)
        print(pos)
        field[pos] = BEACON

        printField(field)

        if dryRun:
            drawSensorField(completeField, sensor)

    for sensor in sensors:
        pos = (sensor['pos'][1], sensor['pos'][0])
        completeField[pos] = SENSOR

    for beacon in beacons:
        pos = (beacon['pos'][1], beacon['pos'][0])
        completeField[pos] = BEACON

    printField(completeField)

    print("-----------------------------------")

    printFieldOfInterest(completeField, yoi)

    i=0
    for e in field[yoi,:]:
        if e not in [0, BEACON]:
            i += 1

    print(f"Answer: {i}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

if __name__=="__main__":
    part1(dryRun = True)
    part2(dryRun = True)
