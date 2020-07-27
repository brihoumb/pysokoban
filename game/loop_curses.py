# -*- coding: utf-8 -*-
'''
Core for control.
'''

import sys
import math
import time
import curses

from guppy import hpy

from controller import Keypad, Coordinate
from core import get_map, check_win, check_crates


def debug(stdscr, player, crates, y, /):
    trace = str(hpy().heap()).split('\n')
    stdscr.addstr(y, 0, f'{player.x}:{player.y}')
    j = y + 1
    for crate in crates:
        stdscr.addstr(j, 0, f'{crate.x}:{crate.y} {crate.validate}')
        j += 1
    for line in trace:
        stdscr.addstr(j, 0, line)
        j += 1


def map_error(ok, /):
    sys.tracebacklimit = 0
    if ok[0] == 1:
        raise Exception('Number of crates should be '
                        + 'equal to number of zone.')
    elif ok[0] == 2:
        raise Exception('No crates found.')
    elif ok[0] == 3:
        raise Exception('No player found.')
    if ok[0] == 4:
        raise Exception('Map size not specified.')


def game_loop(maps, rounds, dbg, /):
    keypad = Keypad()
    stdscr = init_screen()
    start = time.perf_counter()
    for i in range(rounds):
        (map, player, crates, ok) = get_map(maps, i)
        if not ok[1]:
            end_game(stdscr)
            map_error(ok)
        while True:
            display(map, player, crates, stdscr)
            if dbg:
                debug(stdscr, player, crates, map.size.y + 1)
            try:
                c = stdscr.getch()
            except KeyboardInterrupt:
                c = keypad.leave
            if c == keypad.leave:
                return end_game(stdscr)
            elif c == keypad.reset:
                (map, player, crates, ok) = get_map(maps, i)
                if not ok[1]:
                    end_game(stdscr)
                    map_error(ok)
            else:
                move(c, keypad, map, player, crates)
            if not check_win(stdscr, crates):
                break
    win_screen(stdscr, time.perf_counter() - start)
    time.sleep(10)
    end_game(stdscr)
    return 0


def move(c, keypad, map, player, crates, /):
    if c == keypad.up:
        if not map.check_wall(player + Coordinate(0, -1)) and\
           not check_crates(player, crates, map, Coordinate(0, -1)):
            player.y -= 1
            map.update([player, 'P'])
    elif c == keypad.down:
        if not map.check_wall(player + Coordinate(0, 1)) and\
           not check_crates(player, crates, map, Coordinate(0, 1)):
            player.y += 1
            map.update([player, 'P'])
    elif c == keypad.left:
        if not map.check_wall(player + Coordinate(-1, 0)) and\
           not check_crates(player, crates, map, Coordinate(-1, 0)):
            player.x -= 1
            map.update([player, 'P'])
    elif c == keypad.right:
        if not map.check_wall(player + Coordinate(1, 0)) and\
           not check_crates(player, crates, map, Coordinate(1, 0)):
            player.x += 1
            map.update([player, 'P'])


def display(map, player, crates, stdscr, /):
    map.clear()
    i = 0
    for row in map.map:
        stdscr.addstr(i, 0, row)
        [stdscr.addstr(i, index, '#', curses.color_pair(5)) for index
         in range(len(row)) if row.startswith('#', index)]
        [stdscr.addstr(i, index, 'O', curses.color_pair(4)) for index
         in range(len(row)) if row.startswith('O', index)]
        i += 1
    for crate in crates:
        map.update([crate, 'X'])
        stdscr.addstr(crate.y, crate.x, 'X',
                      curses.color_pair(3 if crate.validate else 2))
    map.update([player, 'P'])
    stdscr.addstr(player.y, player.x, 'P', curses.color_pair(1))
    stdscr.refresh()


def win_screen(stdscr, chrono):
    stdscr.erase()
    stdscr.addstr(0, 1, '-' * 39, curses.color_pair(6))
    stdscr.addstr(20, 1, '-' * 39, curses.color_pair(6))
    for i in range(0, 41, 5):
        stdscr.addstr(0, i, '*', curses.color_pair(7))
        stdscr.addstr(20, i, '*', curses.color_pair(7))
    for i in range(1, 20):
        if i % 5 == 0:
            stdscr.addstr(i, 0, '*', curses.color_pair(7))
            stdscr.addstr(i, 40, '*', curses.color_pair(7))
        else:
            stdscr.addstr(i, 0, '|', curses.color_pair(6))
            stdscr.addstr(i, 40, '|', curses.color_pair(6))
    stdscr.addstr(9, 16, '-= WoW =-', curses.color_pair(6))
    stdscr.addstr(10, 9, 'Congratulation you won!!', curses.color_pair(6))
    stdscr.addstr(11, 8, f'You did it in: {int(math.floor(chrono)/60):02d}:' +
                         f'{math.floor(chrono):02d}.' +
                         f'{str(round(chrono, 4)).split(".")[1]}!',
                  curses.color_pair(6))
    stdscr.refresh()


def init_screen():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    stdscr.keypad(True)
    return stdscr


def end_game(stdscr):
    stdscr.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.curs_set(True)
    curses.endwin()
