#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day16_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\n',
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA\n',
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB\n',
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE\n',
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD\n',
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG\n',
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH\n',
    'Valve HH has flow rate=22; tunnel leads to valve GG\n',
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ\n',
    'Valve JJ has flow rate=21; tunnel leads to valve II\n',
]

def dijkstra(rooms, startRoom):

    unvisitedNodes = copy.copy(rooms)

    routes = {}

    for room, d in rooms.items():
        if room == startRoom:
            routes[room] = {'len': 0, 'via': []}
        else:
            routes[room] = {'len': np.inf, 'via': []}

    via = []
    distToStart = 1

    while len(unvisitedNodes) != 0:
        # Take node with smallest distance from routes
        lroutes = [{'name': n, 'len': d['len']} for n, d in routes.items()]
        lroutes = sorted(lroutes, key=lambda a: a['len'])

        for i in range(len(lroutes)):
            if lroutes[i]['name'] in unvisitedNodes:
                currentNode = lroutes[i]['name']
                break

        # Consider all UNVISITED neighbors
        neighbours = [n for n in rooms[currentNode]['neighbours'] if n in unvisitedNodes]

        for neighbour in neighbours:
            distToStart = routes[currentNode]['len'] + 1
            via = routes[currentNode]['via'] + [currentNode]
            neighbourRoom = rooms[neighbour]

            # Check if the distance is better
            if distToStart < routes[neighbour]['len']:
                routes[neighbour]['len'] = distToStart
                routes[neighbour]['via'] = via
            else:
                continue

        del unvisitedNodes[currentNode]

    return routes

def valvesPossible(rooms, currentRoom):

    roomsWithValves = []

    for room, d in rooms.items():
        if d['valve'] == False:
            roomsWithValves.append({'name':room, 'flow':d['flow']})
            roomsWithValves[-1]['tto'] = currentRoom['routes'][room]['len'] + 1

    roomsWithValves = sorted(roomsWithValves, key=lambda a: a['tto'])

    return roomsWithValves

def runSimulation_single(time_left, rooms, currentRoom):
    localOpenValves = []

    while time_left > 0:
        valves = valvesPossible(rooms, currentRoom)

        if len(valves) == 0:
            break

        # Determine time it takes to open all valves => this time +1 is the consideration
        timeToConsider = valves[-1]['tto'] + 1

        # Calculate the pressure all valves would release in this time
        for valve in valves:
            valve['releasedPressure'] = ((timeToConsider - valve['tto']) * valve['flow'])
            valve['heuristic'] = valve['releasedPressure']

        valves = sorted(valves, key=lambda a: a['heuristic'])

        if (len(valves) > 1 and valves[-1]['heuristic'] - valves[-2]['heuristic'] < 12):
            #Use valve with lower tto
#            if valves[-1]['tto']
            valveChosen = valves[-2]
        else:
            valveChosen = valves[-1]

        valveChosen = valves[-1]

        print()
        print(f"Valves: {valves}")
        print()

        time_left -= valveChosen['tto']
        rooms[valveChosen['name']]['valve'] = True
        currentRoom = rooms[valveChosen['name']]

        valveChosen['timeOpened'] = 30-time_left
        localOpenValves.append(valveChosen)

    return localOpenValves


def runSimulation(time_left, rooms, currentRoom, openValves, parentOpenValves=[]):
    openValves.append(copy.deepcopy(parentOpenValves))
    localOpenValves = openValves[-1]

    while time_left > 0:
        valves = valvesPossible(rooms, currentRoom)

        if len(valves) == 0:
            break

        # Determine time it takes to open all valves => this time +1 is the consideration
        timeToConsider = valves[-1]['tto'] + 1

        # Calculate the pressure all valves would release in this time
        for valve in valves:
            valve['releasedPressure'] = ((timeToConsider - valve['tto']) * valve['flow'])

        valves = sorted(valves, key=lambda a: a['releasedPressure'])

        # If the difference in releasedpressure of the two highest is less than the difference in flow rate -> algo can't decide, need to lauch another simulation
        if ( (len(valves) >= 2) and ((valves[-1]['releasedPressure'] - valves[-2]['releasedPressure']) <= valves[-2]['flow'] )):

            alt_valves = copy.deepcopy(valves)

            alt_time_left = time_left - alt_valves[-2]['tto']

            alt_rooms = copy.deepcopy(rooms)
            alt_rooms[alt_valves[-2]['name']]['valve'] = True

            alt_currentRoom = alt_rooms[alt_valves[-2]['name']]

            alt_valves[-2]['timeOpened'] = 30-alt_time_left

            alt_localOpenValves = copy.deepcopy(localOpenValves)
            alt_localOpenValves.append(alt_valves[-2])

            runSimulation(alt_time_left, alt_rooms, alt_currentRoom, openValves, parentOpenValves=alt_localOpenValves)

        time_left -= valves[-1]['tto']
        rooms[valves[-1]['name']]['valve'] = True
        currentRoom = rooms[valves[-1]['name']]

        valves[-1]['timeOpened'] = 30-time_left
        localOpenValves.append(valves[-1])

    return


def runSimulation_2(time_left, rooms, currentRoom, openValves, parentOpenValves=[]):
    openValves.append(copy.deepcopy(parentOpenValves))
    localOpenValves = openValves[-1]

    while time_left > 0:
        valves = valvesPossible(rooms, currentRoom)

        if len(valves) == 0:
            break

        # Determine time it takes to open all valves => this time +1 is the consideration
#        timeToConsider = valves[-1]['tto'] + 1

        for i in range(len(valves)):
            alt_valves = copy.deepcopy(valves)

            alt_time_left = time_left - alt_valves[i]['tto']

            alt_rooms = copy.deepcopy(rooms)
            alt_rooms[alt_valves[i]['name']]['valve'] = True

            alt_currentRoom = alt_rooms[alt_valves[i]['name']]

            alt_valves[i]['timeOpened'] = 30-alt_time_left

            alt_localOpenValves = copy.deepcopy(localOpenValves)
            alt_localOpenValves.append(alt_valves[i])

            runSimulation_2(alt_time_left, alt_rooms, alt_currentRoom, openValves, parentOpenValves=alt_localOpenValves)
    return


def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    rooms = {}

    for l in lines:
        l = re.sub('Valve ', '', l[:-1])
        l = re.sub(' has flow rate=', ',', l)
        l = re.sub('; tunnel', '', l)
        l = re.sub('s', '', l)
        l = re.sub(' lead to valve ', ',', l)
        l = re.sub(' ', '', l)

        o = re.split(',', l)

        if int(o[1]) == 0:
            rooms[o[0]] = {'flow': int(o[1]), 'valve': True, 'timeOpened': 30, 'neighbours': o[2:]}
        else:
            rooms[o[0]] = {'flow': int(o[1]), 'valve': False, 'neighbours': o[2:]}


    for room in rooms:
        routes = dijkstra(rooms, room)
        rooms[room]['routes'] = routes

    time_left = 30
    currentRoom = rooms['AA']

    openValves = runSimulation_single(time_left, rooms, currentRoom)
    releasedPressure = sum([v['flow']*(30-v['timeOpened']) for v in openValves])
    print(f"Answer: {releasedPressure}")


    # simRuns = [[]]

    # runSimulation(time_left, rooms, currentRoom, simRuns)

    # releasedPressure = []

    # for sim in simRuns:
    #     releasedPressure.append({'run':sim, 'releasedPressure': sum([v['flow']*(30-v['timeOpened']) for v in sim])})

    # releasedPressure = sorted(releasedPressure, key=lambda a: a['releasedPressure'])
    # print(f"Answer: {releasedPressure[-1]['releasedPressure']}")

    # AOC:
    # @ 2 -> open DD
    # @ 5 -> open BB
    # @ 9 -> open JJ
    # @17 -> open HH
    # @21 -> open EE
    # @24 -> open CC

    # ME:
    # @ 2 -> open DD OK
    # @ 6 -> open JJ
    # @10 -> open BB
    # @17 -> open HH OK
    # @21 -> open EE OK
    # @24 -> open CC OK

    # Submission: 1510 too low

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

if __name__=="__main__":
    part1(dryRun = True)
    part2(dryRun = True)
