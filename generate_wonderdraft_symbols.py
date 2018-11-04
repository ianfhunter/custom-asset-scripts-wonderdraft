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

if platform.system() == 'Windows':
    RASTER_ENGINE = 'INKSCAPE'
    RASTER_ENGINE = 'SVGLIB'
    RASTER_ENGINE = 'IMAGEMAGICK'
else:
    RASTER_ENGINE = 'CAIROSVG'
    # RASTER_ENGINE = 'CAIRO'


args = genWonderDraftUI()

engine = getEngine(RASTER_ENGINE, args)

createFolders()

ensurePopulated(SVG_DIR)

filenames = getAllFilesInDir(".svg", SVG_DIR)

prefix = ""

if args.is_tree_mode:

    files = getAllFilesInDir(".svg", SVG_DIR)
    for f in tqdm(files):

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
    for f in tqdm(files):
    
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
