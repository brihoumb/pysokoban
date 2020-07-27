# -*- coding: utf-8 -*-
'''
Coordinate, crate and keypad class.
'''

from dataclasses import dataclass


@dataclass
class Keypad:
    up: int = 259
    down: int = 258
    left: int = 260
    right: int = 261
    reset: int = 114
    leave: int = 113


@dataclass
class Coordinate():
    x: int
    y: int

    def __post_init__(self):
        self.x = int(self.x)
        self.y = int(self.y)

    def __add__(self, term):
        return Coordinate(self.x + term.x, self.y + term.y)

    def __iadd__(self, term):
        return Coordinate(self.x + term.x, self.y + term.y)

    def __sub__(self, term):
        return Coordinate(self.x - term.x, self.y - term.y)

    def __isub__(self, term):
        return Coordinate(self.x - term.x, self.y - term.y)

    def __eq__(self, term):
        return True if self.x == term.x and self.y == term.y else False

    def __ne__(self, term):
        return True if self.x != term.x or self.y != term.y else False


class Crate():
    def __init__(self, x, y, /):
        self.__validate = False
        self.__coordinate = Coordinate(x, y)

    @property
    def x(self):
        return self.__coordinate.x

    @property
    def y(self):
        return self.__coordinate.y

    @property
    def validate(self):
        return self.__validate

    @validate.setter
    def validate(self, state):
        del self.__validate
        self.__validate = state

    def check_position(self, pos, /):
        if self.__coordinate == pos:
            return 1
        return 0

    def move(self, direction, /):
        self.__coordinate += direction

    def __add__(self, term):
        return Coordinate(self.__coordinate.x + term.x,
                          self.__coordinate.y + term.y)
