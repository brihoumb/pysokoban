#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Main function with argument parsing.
'''

import os
import sys
import argparse

import game.loop_curses as tui


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid path")


def main():
    parser = argparse.ArgumentParser(description='Generate sokoban game.')
    parser.add_argument('-g', '--graphic', action='store_true',
                        help='use GUI instead of Curse.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='debug mode.')
    parser.add_argument('rounds', metavar='Rounds',
                        type=int, help='number of round to play.')
    parser.add_argument('maps', metavar='Maps',
                        type=dir_path, help='path where maps are stored.')
    args = parser.parse_args()
    if args.rounds > len([name for name in os.listdir(args.maps)
                         if name.endswith('.skb')]):
        sys.tracebacklimit = 0
        raise Exception('Cannot have more rounds than maps.')
    if args.graphic:
        pass
    else:
        return tui.game_loop(args.maps, args.rounds, args.debug)
    return 0


if __name__ == '__main__':
    sys.exit(main())
