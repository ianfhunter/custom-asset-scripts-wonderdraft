import os
import glob
import platform
from config import *

def createFolders():
    for x in [SVG_DIR, SYMBOL_DIR, TREE_DIR]:
        if not (os.path.exists(x) and os.path.isdir(x)):
            os.mkdir(x)


def getAllFilesInDir(filetype, directory):
    files = []
    for r, d, f in os.walk(directory):
        for file in f:
            if filetype in file:
                files.append(os.path.join(r, file))

    return files


def getFileName(path, no_ext=False):
    sep = file_seperator()
    a = path.split(sep)[-1]
    if no_ext:
        a = ".".join(str(x) for x in a.split(".")[:-1])
    return a


def removeBaseFolder(path):
    sep = file_seperator()
    s = path.split(sep)
    if platform.system() == 'Windows':
        split_at = 1
    else:
        split_at = 2
    s = sep.join(str(x) for x in s[split_at:])
    if len(s) > 0 and s[0] == " ":
        s = s[1:]
    return s


def saveWrite(toWrite, path):

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    if toWrite is not None:
        with open(path, 'w') as of:
            of.write(toWrite)


def ensurePopulated(path):
    if (len(os.listdir(path)) == 0):
        print(path + " folder that should contain files is empty.")


def readColorSchemeFile():
    return [
        {
            'name': s[0],
            'variant': s[1],
            'colors': s[2:]
        }
        for s in [
            l.strip().split(',')
            for l in open(COLOR_SCHEME_FILE).readlines()
            if l.strip()[0] != '#'
        ]
    ]


def getCategory(folder, color_scheme_entry):
    design_name = color_scheme_entry['name']
    variant = color_scheme_entry['variant'].upper()
    return f'{folder} {design_name} {variant}'


def file_seperator():
    if platform.system() == 'Windows':
	    return "\\"
    else:
        return "/"


def splitPath(path, no_cat=False):
    x = getFileName(path)

    sep = file_seperator()

    if no_cat:
        subdir = path.split(sep)[:-1]
        subdir = sep.join(str(f) for f in subdir)
        s = removeBaseFolder(subdir)

        return x, None, s
    else:

        if platform.system() == 'Windows':
            split_at = 1
        else:
            split_at = 2

        category = path.split(sep)[split_at]

        subdir = path.split(sep)[1:-1]
        subdir = sep.join(str(f) for f in subdir)

        s = removeBaseFolder(subdir)

        return x, category, s