import json
import os
import platform
import re
import glob
from pathlib import Path
from raster_engines import getEngine
from file_system import *
from user_interface import *
from tqdm import tqdm
from config import *

def generateWonderDraftSymbols(no_prompt=False):
    if platform.system() == 'Windows':
        RASTER_ENGINE = 'INKSCAPE'
        RASTER_ENGINE = 'SVGLIB'
        RASTER_ENGINE = 'IMAGEMAGICK'
    else:
        RASTER_ENGINE = 'CAIROSVG'
        RASTER_ENGINE = 'RSVG'
        # RASTER_ENGINE = 'CAIRO'
        #RASTER_ENGINE = 'SVGLIB'

    args = genWonderDraftUI(no_prompt=no_prompt)

    engine = selectEngine(args, no_prompt=no_prompt)
    # engine = getEngine(RASTER_ENGINE, args)

    createFolders()

    ensurePopulated(SVG_DIR)

    filenames = getAllFilesInDir(".svg", SVG_DIR)

    prefix = ""

    if no_prompt:
        tqdm_out = open(PROGRESS_TRACKER_PNG_TMP_FILE, "w")
    else:
        tqdm_out = None


    if args.is_tree_mode:

        files = getAllFilesInDir(".svg", SVG_DIR)
        for f in tqdm(files, file=tqdm_out):

            basefile, category, s = splitPath(f)

            file_name = f'{prefix}{TREE_DIR}/{category}/{s}/{basefile}.svg'

            png_path = os.path.join(file_name.replace('svg', 'png'))

            svg_path = os.path.join(f)

            saveWrite(None, png_path)
            engine.convert(
                svg_path,
                png_path
            )

    else:
        # Ensure the output directory exists


        files = getAllFilesInDir(".svg", SVG_DIR)
        for f in tqdm(files, file=tqdm_out):

            basefile, category, s = splitPath(f)
            file_name = removeBaseFolder(f)

            svg_path = os.path.join(f)
            png_path = os.path.join(
                SYMBOL_DIR, file_name.replace('svg', 'png'))

            saveWrite(None, png_path)
            engine.convert(
                svg_path,
                png_path
            )

if __name__ == "__main__":
    generateWonderDraftSymbols()
