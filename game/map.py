# -*- coding: utf-8 -*-
'''
Map controler.
'''

import sys

from controller import Coordinate, Crate


class Map():
    def __init__(self, map, size, /):
        self.__map = map
        self.__size = size
        self.__origin = map
        for i in range(size.y):
            if len(map[i]) != size.x:
                map[i] += ' ' * (size.x - len(map[i]))

    @property
    def size(self):
        return self.__size

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, map):
        del self.__map
        self.__map = map

    def check_wall(self, pos):
        if pos.x >= self.__size.x or pos.y >= self.__size.y\
           or self.__map[pos.y][pos.x] == '#' or pos.x < 0 or pos.y < 0:
            return 1
        return 0

    def clear(self):
        del self.__map
        self.__map = self.__origin.copy()

    def update(self, *coordinates):
        for coordinate in coordinates:
            self.__map[coordinate[0].y] = replace(self.__map[coordinate[0].y],
                                                  coordinate[1],
                                                  coordinate[0].x)

    def valide_spot(self, pos):
        if self.__map[pos.y][pos.x] == 'O':
            return 1
        return 0


def replace(str, char, x, /):
    tmp = list(str)
    tmp[x] = char
    return ''.join(tmp)


def parse(map_path):
    parsed_map = open(map_path, 'r').read().splitlines()
    (size, player, *crates) = [s.split(':') for s in parsed_map[0].split(';')]
    if size[1] != len(parsed_map) - 1:
        size = (size[0], str(len(parsed_map) - 1))
    player = (Coordinate(player[0], player[1]) if len(player) == 2 and
              player[0].isdigit() and player[1].isdigit() else None)
    if len(size) == 2 and size[0].isdigit() and size[1].isdigit():
        map = Map(parsed_map[1:], Coordinate(size[0], size[1]))
    else:
        map = Map(parsed_map[1:], Coordinate(0, 0))
    crates = [Crate(crate[0], crate[1]) for crate in crates
              if len(crate) == 2 and crate[0].isdigit() and crate[1].isdigit()]
    return (map, player, crates)
