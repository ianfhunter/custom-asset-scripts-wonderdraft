import itertools
import os
import re
from file_system import *
from user_interface import *
from tqdm import tqdm

args = genSVGUI()

TEMPLATE_COLORS = ['cf211b', '64c93f', '4b90e5']

print("Initial variables have been created!")

if args.prefix is None:
    prefix_request = input("Please enter the PREFIX for all new permutations: ")
    print("You entered " + str(prefix_request) +
        " as the PREFIX for all new permutations")
else:
    prefix_request = args.prefix

prefix = prefix_request

# Ensure the output directory exists
createFolders()

print("Processing permutations please wait... ")

color_schemes = readColorSchemeFile()

template_filenames = getAllFilesInDir(".svg", TEMPLATE_DIR)

# For each of the template files
for fn in tqdm(template_filenames):

    """
        # # Extract the number of the design we're operating on
        # path_and_name = fn_noT.split('.svg')[0]  # Get file name without extension
        # base_filename = getFileName(path_and_name)

        # base_multisymb_str = base_filename.split(' ')
        # multisymb_str = path_and_name.split(' ')

        # # Get last part of that and check if it has a number
        # trail_str = base_multisymb_str[-1]

        # multi_symbol = False
        # if any(char.isdigit() for char in trail_str):
        #     multi_symbol = True
    """

    # Read in the master SVG
    with open(os.path.join(fn)) as f:
        svg_in = f.read()
        slot_colors = [t for t in TEMPLATE_COLORS if t in svg_in]
        num_colors = len(slot_colors)


    for x in color_schemes:

        p_num = 1

        c = getCategory("", x)

        print(fn)
        basefileext, _, s = splitPath(fn, no_cat=True)
        # print("category: ", c)
        # print("basefileext: ", basefileext)
        # print("subdir: ", s)

        # Generate all of the applicable permutations of the current color scheme
        # (n=3 for one slot, n=6 for two or three slots)
        color_permutations = list(
            itertools.permutations(x['colors'], num_colors))

        # Generate a new SVG for each permutation
        for perm in color_permutations:
            svg_out = svg_in
            for (t, z) in zip(slot_colors, perm):
                svg_out = svg_out.replace(t, z)

            # Detect if MultiSymbol or not
            basefile = getFileName(fn, no_ext=True)
            # print("basefile: ", basefile)
            trail_str = basefile[-1]

            multi_symbol = True
            # multi_symbol = False
            # if any(char.isdigit() for char in trail_str):
            #     multi_symbol = True

            if multi_symbol:
                file_name = f'{prefix}{SVG_DIR}/{c}/{s}/{c} {basefile}-{p_num}.svg'
            else:
                file_name = f'{prefix}{SVG_DIR}/{c}/{s}/{c} {basefile}.svg'

            file = file_name
            saveWrite(svg_out, file)

            p_num += 1

print("All permutations have been created!")
