import os
import glob
import platform
from config import *
import yaml
import lxml.etree as etree
import re


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
    d=False
    if "/" in path or "\\" in path:
        d=True
    if not os.path.exists(os.path.dirname(path)) and d:
        os.makedirs(os.path.dirname(path))

    if toWrite is not None:
        with open(path, 'w') as of:
            of.write(toWrite)


def ensurePopulated(path):
    if (len(os.listdir(path)) == 0):
        print(path + " folder that should contain files is empty.")


def readColorSchemeFile_Colors(file=COLOR_SCHEME_FILE):
    x = [
        {
            'color_replacements': s
        }
        for s in [
            l[1:].strip().split(',')
            for l in open(file).readlines()
            if len(l.strip()) > 0 and l.strip()[0] == '>'
        ]
    ]

    if len(x) == 0:
        return TEMPLATE_COLORS
    else:
        print("Colors Found: ", x[0]['color_replacements'])
        return [z.strip() for z in x[0]['color_replacements']]


def readColorSchemeFile_Themes(file=COLOR_SCHEME_FILE):

    return [
        {
            'name': s[0],
            'variant': s[1],
            'colors': s[2:]
        }
        for s in [
            l.strip().split(',')
            for l in open(file).readlines()
            if len(l.strip()) > 0 and l.strip()[0] not in ['#', '>']
        ]
    ]

def parseThemeFile(file=THEME_FILE):

    with open(THEME_FILE, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print("Theme File Parse Error")
            quit()




def getCategory(folder, color_scheme_entry):
    design_name = color_scheme_entry['name']
    variant = color_scheme_entry['variant'].upper()
    print(folder+"|"+design_name+"|"+variant)
    return f'{folder}{design_name} {variant}'


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


def stripBackground(file):
    # For City maps mostly
    dom1 = etree.parse(file)  # parse an XML file by name
    a = dom1.xpath('//*[@id="background"]')
    if(len(a) > 0):
        p = a[0].getparent()
        p.remove(a[0])
        print("Stripping Background from image: ", file)
        dom1.write(file, pretty_print=True)


def replaceColor(f, old, new, amount=0):
    colorMatch = re.compile(old, re.IGNORECASE)
    new_f = colorMatch.sub(new, f, amount)
    return new_f
