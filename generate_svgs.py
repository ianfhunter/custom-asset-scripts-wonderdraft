import itertools
import os
import re
from file_system import *
from user_interface import *
from tqdm import tqdm
from config import *



def generateSVGs(args, gui=False):

    if not gui:
        print("Initial variables have been created!")


    # Ensure the output directory exists
    createFolders()

    if not gui:
        print("Processing permutations please wait... ")
        

    if hasattr(args, 'color_scheme') and args.color_scheme is not "":
        color_schemes = readColorSchemeFile_Themes(file=args.color_scheme)
    else:
        color_schemes = readColorSchemeFile_Themes()

    print("color_schemes",color_schemes)

    template_filenames = getAllFilesInDir(".svg", TEMPLATE_DIR)

    # For each of the template files
    if gui:
        tqdm_out = open(PROGRESS_TRACKER_SVG_TMP_FILE, "w")
    else:
        tqdm_out = None

    for fn in tqdm(template_filenames, file=tqdm_out):

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
            slot_colors = [t for t in readColorSchemeFile_Colors() if t in svg_in]
            print("SLOT COLORS:", slot_colors)
            num_colors = len(slot_colors)


        for i, x in enumerate(color_schemes):

            if args.quick and i > 0:
                print("skup")
                continue

            p_num = 1

            c = getCategory("", x)

            if not gui:
                print(fn)
            basefileext, _, s = splitPath(fn, no_cat=True)
            # print("category: ", c)
            # print("basefileext: ", basefileext)
            # print("subdir: ", s)

            # Generate all of the applicable permutations of the current color scheme
            # (n=3 for one slot, n=6 for two or three slots)
            color_permutations = list(
                itertools.permutations(x['colors'], num_colors))

            print(x)
            print("color_permutations:", color_permutations)

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

                args.prefix = ""    # TODO: BUG

                if multi_symbol:
                    file_name = f'{args.prefix}{SVG_DIR}/{c}/{s}/{c} {basefile}-{p_num}.svg'
                else:
                    file_name = f'{args.prefix}{SVG_DIR}/{c}/{s}/{c} {basefile}.svg'

                file = file_name
                saveWrite(svg_out, file)

                p_num += 1

    if not gui:
        print("All permutations have been created!")
    return True


if __name__ == "__main__":

    args = genSVGUI()
    generateSVGs(args)
