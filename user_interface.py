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


def genWonderDraftUI():
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

    while mode_input != 's' and mode_input != 't':
        mode_input = input('Operate in (S)ymbol mode or (T)ree mode? ').lower()

    if mode_input == 't':
        args.is_tree_mode = True
    else:
        args.is_tree_mode = False


    # Maximum Dimension Size
    mode_input = args.max_dim
    if args.max_dim is None:
        while mode_input not in ['n', 'no', -1] and not is_number(mode_input):
            mode_input = input('Maximum Output Dimension Size: Number or (NO): ').lower()

    if mode_input in ['n', 'no', 0] or not is_number(mode_input):
        if not is_number(mode_input):
            print("max-dim unrecognized, turning off.", mode_input)
        args.max_dim = -1
    else:
        args.max_dim = int(mode_input)

    return args


def genSVGUI():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", help="Prefix", default=None, type=str)
    parser.add_argument("-q", "--quick", help="Only generate one color permutation per theme", action="store_true")
    args = parser.parse_args()

    if args.quick == False:
        mode_input = "Q"
        while mode_input not in ['y', 'n']:
            mode_input = input('Complete (Y) or Quick(N) Generation: ').lower()

        if mode_input == 'y':
            args.quick = True

    if args.prefix is None:
        prefix_request = input("Please enter the PREFIX for all new permutations: ")
        print("You entered " + str(prefix_request) +
            " as the PREFIX for all new permutations")
    else:
        prefix_request = args.prefix

    args.prefix = prefix_request

    return args


possible_engines = None
supported_engines = None
unsupported_engines = None


def getEngineSpecs():
    global possible_engines
    global supported_engines
    global unsupported_engines
    return possible_engines, supported_engines, unsupported_engines


def initEngineSupport(args):
    global possible_engines
    global supported_engines
    global unsupported_engines

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


def selectEnginePrompt(args):

    choice = "N/A"
    print("Inactive Rasterizing Engines: ")
    for x in unsupported_engines:
        print("*", x.name)
    print("Available Rasterizing Engines: ")

    while not is_number(choice) or int(choice) > len(supported_engines):
        for x in range(len(supported_engines)):
            print("(" + str(x) + ")", supported_engines[x].name)
        choice = input('Please Select an engine: ')

    return selectEngine(choice)


def selectEngine(choice):
    global supported_engines

    return supported_engines[int(choice)]