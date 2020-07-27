# -*- coding: utf-8 -*-
'''
Game core controler.
'''

import os

from map import parse


def check_crates(pos, crates, map, dir, /, loop=False):
    for crate in crates:
        if not loop\
           and crate.check_position(pos + dir)\
           and not map.check_wall(crate + dir)\
           and not check_crates(crate, crates, map, dir, True):
            crate.move(dir)
            crate.validate = True if map.valide_spot(crate) else False
            return 0
        elif crate.check_position(pos + dir):
            return 1
    return 0


def check_win(stdscr, crates, /):
    win = 0
    for crate in crates:
        if crate.validate:
            win += 1
    if win == len(crates):
        return 0
    return 1


def get_map(maps, index, /):
    (map, player, crates) = parse(os.path.join(maps, os.listdir(maps)[index]))
    return (map, player, crates, is_valide(len(crates), map, player))


def is_valide(n_crates, map, player, /):
    n_point = 0
    for row in map.map:
        n_point += row.count('O')
    if n_point != n_crates:
        return (1, False)
    elif n_crates == 0:
        return (2, False)
    elif player is None:
        return (3, False)
    elif map.size.x == 0 or map.size.y == 0:
        return (4, False)
    else:
        return (0, True)
