import os
import glob
import argparse
from raster_engines import *


def is_number(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def genWonderDraftUI(no_prompt=False):
    # Commandline
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", help="generate symbols (all \
        in one folder) ", action="store_true")
    parser.add_argument("-t", "--tree", help="generate trees (each \
        style in its own folder for automatic variation)", action="store_true")
    parser.add_argument("-x", "--max-dim", help="limit the output dimensions to a specific size", default=None, type=str)

    args = parser.parse_args()

    # User Prompts as backup

    if args.symbol:
        mode_input = 's'
    elif args.tree:
        mode_input = 't'
    else:
        mode_input = 'invalid'

    # Mode of Operation
    if no_prompt:
        #Default for now
        mode_input = 't'
    else:
        while mode_input != 's' and mode_input != 't':
            mode_input = input('Operate in (S)ymbol mode or (T)ree mode? ').lower()

    if mode_input == 't':
        args.is_tree_mode = True
    else:
        args.is_tree_mode = False


    # Maximum Dimension Size
    if no_prompt:
        args.max_dim = -1
    else:
        mode_input = args.max_dim
        if args.max_dim is None and no_prompt is False:
            while mode_input not in ['n', 'no', -1] and not is_number(mode_input):
                mode_input = input('Maximum Output Dimension Size: Number or (NO): ').lower()

        if mode_input in ['n', 'no', 0] or not is_number(mode_input):
            if not is_number(mode_input):
                print("max-dim unrecognized, turning off.", mode_input)
            args.max_dim = -1
        else:
            args.max_dim = int(mode_input)

    return args


def genSVGUI(no_prompt=False):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", help="Prefix", default=None, type=str)
    parser.add_argument("-q", "--quick", help="Only generate one color permutation per theme", action="store_true")
    args = parser.parse_args()

    if args.quick == False and no_prompt is False:
        mode_input = "Q"
        while mode_input not in ['y', 'n']:
            mode_input = input('Complete (Y) or Quick(N) Generation: ').lower()

        if mode_input == 'y':
            args.quick = True


    return args


def selectEngine(args, no_prompt=False):

    possible_engines = [
        cairoSVGRE(),
        imageMagickRE(),
        inkscapeRE(),
        cairoRE(),
        svglibRE(),
        rsvgRE()
    ]

    supported_engines = []
    unsupported_engines = []

    for e in possible_engines:
        try:
            e.load(args)
            supported_engines.append(e)
        except:
            unsupported_engines.append(e)

    choice = "N/A"
    if no_prompt:
        #Default for now
        choice = 0
    else:
        print("Inactive Rasterizing Engines: ")
        for x in unsupported_engines:
            print("*", x.name)
        print("Available Rasterizing Engines: ")

        while not is_number(choice) or int(choice) > len(supported_engines):
            for x in range(len(supported_engines)):
                print("("+str(x)+")", supported_engines[x].name)
            choice = input('Please Select an engine: ')

    return supported_engines[int(choice)]