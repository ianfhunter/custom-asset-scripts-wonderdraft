import json
import os
import platform
import re
import glob
from pathlib import Path
from raster_engines import getEngine

if platform.system() == 'Windows':
    RASTER_ENGINE = 'INKSCAPE'  
    RASTER_ENGINE = 'IMAGEMAGICK'  
    RASTER_ENGINE = 'SVGLIB'        
else:
    RASTER_ENGINE = 'CAIROSVG'


engine = getEngine(RASTER_ENGINE)

SVG_DIR = './svg_output'
SYMBOL_DIR = './symbols'
TREE_DIR = './trees'


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--symbol", help="Symbol Mode", action="store_true")
parser.add_argument("-t", "--tree", help="Tree Mode", action="store_true")
args = parser.parse_args()



# Prompt the user whether to generate symbols (all in one folder) or trees (each
# style in its own folder for automatic variation)
if args.symbol:
    mode_input = 's'
elif args.tree:
    mode_input = 't'
else:
    mode_input = 'invalid'

while mode_input != 's' and mode_input != 't':
    mode_input = input('Operate in (S)ymbol mode or (T)ree mode? ').lower()

if mode_input == 't':
    is_tree_mode = True
else:
    is_tree_mode = False


if (len(os.listdir(SVG_DIR)) == 0):
    print(SVG_DIR + " folder that should contain SVGs is empty.")

filenames = glob.glob(SVG_DIR + '/**/*.svg', recursive=True)

if is_tree_mode:
    # Ensure the output directory exists
    if not (os.path.exists(TREE_DIR) and os.path.isdir(TREE_DIR)):
        print(f'Making directory {os.path.join(TREE_DIR)}')
        os.mkdir(TREE_DIR)

    SVG_DIR = "./svg_output/"
    categories = [name for name in os.listdir(
        SVG_DIR) if os.path.isdir(SVG_DIR+name)]

    # Create a new directory for each category; each directory becomes a tree
    # symbol entry in Wonderdraft
    for category in categories:
        # Create the category directory if it doesn't already exist
        if not os.path.exists(os.path.join(TREE_DIR, category)):
            print(f'Making directory {os.path.join(TREE_DIR, category)}')
            os.mkdir(os.path.join(TREE_DIR, category))

        # Determine which SVg files belong to this category
        cat_fns = [fn for fn in filenames if category in fn]
        for fn in cat_fns:
            # print(fn)
            if platform.system() == 'Windows':
                file_name = fn.split("\\")[-1]
            else:
                file_name = fn.split("/")[-1]
            engine.convert(
                os.path.join(fn),
                os.path.join(TREE_DIR, category,
                             file_name.replace('svg', 'png'))
            )

else:
    # Ensure the output directory exists
    if (os.path.exists(SYMBOL_DIR) and os.path.isdir(SYMBOL_DIR)):
        print(SYMBOL_DIR, " already exists.")
    else:
        print(f'Making directory {os.path.join(SYMBOL_DIR)}')
        os.mkdir(SYMBOL_DIR)

    SVG_DIR = "./svg_output/"
    categories = [name for name in os.listdir(
        SVG_DIR) if os.path.isdir(SVG_DIR+name)]

    # Just create all the files in the one directory
    for category in categories:

        cat_fns = [fn for fn in filenames if category in fn]
        for fn in cat_fns:

            if platform.system() == 'Windows':
                file_name = fn.split("\\")[-1]
            else:
                file_name = fn.split("/")[-1]

            svg_path = os.path.join(fn)
            png_path = os.path.join(
                SYMBOL_DIR, file_name.replace('svg', 'png'))

            engine.convert(
                svg_path,
                png_path
            )
