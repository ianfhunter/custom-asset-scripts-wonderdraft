import os
import glob
import argparse


def genWonderDraftUI():
    # Commandline
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", help="generate symbols (all \
        in one folder) ", action="store_true")
    parser.add_argument("-t", "--tree", help="generate trees (each \
        style in its own folder for automatic variation)", action="store_true")
    args = parser.parse_args()

    # User Prompt
    if args.symbol:
        mode_input = 's'
    elif args.tree:
        mode_input = 't'
    else:
        mode_input = 'invalid'

    while mode_input != 's' and mode_input != 't':
        mode_input = input('Operate in (S)ymbol mode or (T)ree mode? ').lower()

    if mode_input == 't':
        args.is_tree_mode = True
    else:
        args.is_tree_mode = False

    return args


def genSVGUI():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", help="Prefix", default=None, type=str)
    args = parser.parse_args()
    return args