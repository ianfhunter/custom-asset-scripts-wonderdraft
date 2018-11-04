import os
import glob
import argparse


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


def genWonderDraftUI():
    # Commandline
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", help="generate symbols (all \
        in one folder) ", action="store_true")
    parser.add_argument("-t", "--tree", help="generate trees (each \
        style in its own folder for automatic variation)", action="store_true")
    parser.add_argument("-x", "--max-dim", help="limit the output dimensions to a specific size", default=-1, type=int)

    args = parser.parse_args()

    # User Prompts as backup
    
    if args.symbol:
        mode_input = 's'
    elif args.tree:
        mode_input = 't'
    else:
        mode_input = 'invalid'
    
    # Mode of Operation
    while mode_input != 's' and mode_input != 't':
        mode_input = input('Operate in (S)ymbol mode or (T)ree mode? ').lower()
        
    if mode_input == 't':
        args.is_tree_mode = True
    else:
        args.is_tree_mode = False

    # Maximum Dimension Size
    if args.max_dim == -1:
        while mode_input not in ['n', 'no', -1] and not is_number(mode_input):
            mode_input = input('Maximum Output Dimension Size: Number or (NO): ').lower()
        if mode_input in ['n', 'no'] :
            args.max_dim = -1
        else:
            args.max_dim = int(mode_input)


        
    return args


def genSVGUI():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", help="Prefix", default=None, type=str)
    args = parser.parse_args()
    return args