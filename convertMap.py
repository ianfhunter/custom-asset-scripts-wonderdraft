import json
import os
import platform
import glob
from pathlib import Path
from raster_engines import getEngine
from file_system import *
from user_interface import *
from tqdm import tqdm
from config import *
import random
import math
import itertools

def convertMap(args, gui=False):

    f = args.file
    # max_dim=mdim,
    # engine=self._engine.value,

    if gui:
        tqdm_out = open(PROGRESS_TRACKER_MAP_TMP_FILE, "w")
    else:
        tqdm_out = None

    svg_path = os.path.join(f)
    png_path = os.path.join(
        SYMBOL_DIR, svg_path.replace('svg', 'png'))

    saveWrite(None, png_path)
    args.engine.setMaxDim(args.max_dim)
    args.engine.convert(
        svg_path,
        png_path
    )

def generateMapVariants(args, gui=False):

    createFolders() 

    not_default_file = False
    if hasattr(args, 'file') and args.file is not "":
        tf = parseThemeFile(file=args.file)
    else:
        tf = parseThemeFile()


    template_filenames = getAllFilesInDir(".svg", TEMPLATE_DIR)

    # For each of the template files
    if gui:
        tqdm_out = open(PROGRESS_TRACKER_MAP_TMP_FILE, "w")
    else:
        tqdm_out = None

    # for fn in tqdm(template_filenames, file=tqdm_out):
    for fn in template_filenames:

        stripBackground(os.path.join(fn))

        # Read in the master SVG
        with open(os.path.join(fn)) as f:
            svg_in = f.read()

        basefileext, _, s = splitPath(fn, no_cat=True)


        for theme in tf['themes']:

            reps = tf['replace'] if 'replace' in tf else []
            perms = tf['permute'] if 'permute' in tf else []

            old_path = os.path.join(fn)
            new_path = os.path.join(old_path.replace('templates', MAP_DIR+'/'+theme))

            perm__ = []
            if len(perms) > 0:
                perm_category = list(perms.keys())[0]
                permlist = perms[perm_category]
                if(len(permlist) > 7):
                    print("There are", math.factorial(len(permlist))), "different svgs to produe for one theme. Avoiding computer overload and quitting..."
                    print("Please rethink your theme")
                    quit()
                else:
                    perm__ = list(itertools.permutations(permlist))                    
            else:
                perm__ = [None]


            for p in perm__:

                svg_out = svg_in

                if p is not None:
                    replaceMe = tf['themes'][theme][perm_category]
                    for new, old in zip(replaceMe, p):
                        svg_out = replaceColor(svg_out, old, new)
                
                if 'replace' in tf:
                    for replacement in tf['replace']:

                        old_color = tf['replace'][replacement]
                        try:
                            replacement = tf['themes'][theme][replacement]
                        except KeyError:
                            print("Was asked to replace '"+replacement+"', but theme does not have any themes for it.")

                        if type(replacement) == str:
                            # One-to-One replacement
                            svg_out = replaceColor(svg_out, old_color, replacement)

                        elif type(replacement) == list:
                            # Shuffle replacement
                            while old_color in svg_out:
                                new_color = random.choice(replacement)
                                svg_out = replaceColor(svg_out, old_color, new_color, amount=1)
                        else:
                            print("Err: Unsupported Type in Theme")
                            quit()

                    saveWrite(svg_out, new_path)
                else:
                    saveWrite(svg_out, new_path)
                    

    return True

if __name__ == "__main__":
    args = cityMapUI()
    generateMapVariants(args)