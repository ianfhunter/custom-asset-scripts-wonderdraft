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

def generateWonderDraftSymbols(args, gui=False):

    createFolders()

    ensurePopulated(SVG_DIR)

    filenames = getAllFilesInDir(".svg", SVG_DIR)

    prefix = ""

    if gui:
        tqdm_out = open(PROGRESS_TRACKER_PNG_TMP_FILE, "w")
    else:
        tqdm_out = None

    if hasattr(args, 'folder'):
        SYMBOL_DIR = TREE_DIR = args.folder

    if args.is_tree_mode:

        files = getAllFilesInDir(".svg", SVG_DIR)
        for f in tqdm(files, file=tqdm_out):

            basefile, category, s = splitPath(f)

            file_name = f'{prefix}{TREE_DIR}/{category}/{s}/{basefile}.svg'

            png_path = os.path.join(file_name.replace('svg', 'png'))

            svg_path = os.path.join(f)

            saveWrite(None, png_path)
            args.engine.convert(
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
            args.engine.convert(
                svg_path,
                png_path
            )

if __name__ == "__main__":
    args = genWonderDraftUI()
    initEngineSupport(args)
    args.engine = selectEnginePrompt(args)

    generateWonderDraftSymbols(args)
