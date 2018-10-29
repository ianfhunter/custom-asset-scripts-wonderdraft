import json
import os
import platform
import re

if platform.system() == 'Windows':
  import subprocess
else:
  import cairosvg


SVG_DIR = './svg_output'
SYMBOL_DIR = './symbols'
TREE_DIR = './trees'


def convert(svg_path, png_path):
  if platform.system() == 'Windows':
    subprocess.run([
      r'C:\Program Files\Inkscape\inkscape',
      '-z',
      svg_path,
      '-e',
      png_path
    ])
  else:
    cairosvg.svg2png(url=svg_path, write_to=png_path)


# Prompt the user whether to generate symbols (all in one folder) or trees (each
# style in its own folder for automatic variation)
mode_input = 'foo'
while mode_input != 's' and mode_input != 't':
  mode_input = input('Operate in (S)ymbol mode or (T)ree mode? ').lower()
is_tree_mode = mode_input == 't'

filenames = sorted([
    fn
    for fn in os.listdir(SVG_DIR)
    if os.path.isfile(os.path.join(SVG_DIR, fn)) and '.svg' in fn
])

if is_tree_mode:
  # Ensure the output directory exists
  if not (os.path.exists(TREE_DIR) and os.path.isdir(TREE_DIR)):
    print(f'Making directory {os.path.join(TREE_DIR)}')
    os.mkdir(TREE_DIR)

  # Extract the tree design categories (e.g. 'Flat Design Trees Cold 12a')
  categories = set(
    [re.match(r'(Flat[ _]Design[ _]Trees[ _]\w+[ _]\d+\w)', s).group(1)
      for s in filenames])
  
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
      convert(
        os.path.join(SVG_DIR, fn),
        os.path.join(TREE_DIR, category, fn.replace('svg', 'png'))
      )

else:
  # Ensure the output directory exists
  if not (os.path.exists(SYMBOL_DIR) and os.path.isdir(SYMBOL_DIR)):
    print(f'Making directory {os.path.join(SYMBOL_DIR)}')
    os.mkdir(SYMBOL_DIR)
  
  # Just create all the files in the one directory
  for fn in filenames:
    convert(
        os.path.join(SVG_DIR, fn),
        os.path.join(SYMBOL_DIR, fn.replace('svg', 'png'))
    )
