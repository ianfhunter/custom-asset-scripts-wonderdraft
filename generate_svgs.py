import itertools
import os
import re


COLOR_SCHEME_FILE = './color_schemes.txt'
SVG_TEMPLATE_DIR  = './templates'
SVG_OUTPUT_DIR    = './svg_output'
TEMPLATE_COLORS   = ['cf211b', '64c93f', '4b90e5']

print("Initial variables have been created!")

prefix_request = input("Please enter the PREFIX for all new permutations: ")
print("You entered " + str(prefix_request) + " as the PREFIX for all new permutations")

# Ensure the output directory exists
if not (os.path.exists(SVG_OUTPUT_DIR) and os.path.isdir(SVG_OUTPUT_DIR)):
  os.mkdir(SVG_OUTPUT_DIR)

print("Created/Found Output directoy!")
print("Processing permutations please wait... ")

color_schemes = [
    { 'name': s[0], 'variant': s[1], 'colors': s[2:] } 
    for s in [
        l.strip().split(',')
        for l in open(COLOR_SCHEME_FILE).readlines()
        if l.strip()[0] != '#'
      ]
  ]

template_filenames = sorted([
    fn 
    for fn in os.listdir(SVG_TEMPLATE_DIR)
    if os.path.isfile(os.path.join(SVG_TEMPLATE_DIR, fn)) and '.svg' in fn
  ])

# For each of the template files
for fn in template_filenames:
  print(fn)
  # Extract the number of the design we're operating on
  name_noext = fn.split('.svg')[0] # Get file name without extension
  multisymb_str = name_noext.split(' ')
  trail_str = multisymb_str[-1]  # Get last part of that and check if it has a number
  
  
  multi_symbol = False
  if any(char.isdigit() for char in trail_str):
    multi_symbol = True

    
  # Read in the master SVG
  with open(os.path.join(SVG_TEMPLATE_DIR, fn)) as f:
    svg_in = f.read()

  # Find out which color slots are in the template
  slot_colors = [t for t in TEMPLATE_COLORS if t in svg_in]
  num_colors = len(slot_colors)

  # For each color scheme defined in the color scheme file
  for s in color_schemes:
    design_name = s['name']
    variant = s['variant'].upper()
    
    
    # Generate all of the applicable permutations of the current color scheme
    # (n=3 for one slot, n=6 for two or three slots)
    color_permutations = list(itertools.permutations(s['colors'], num_colors))
    
    p_num = 1
  
    # Generate a new SVG for each permutation
    for perm in color_permutations:
      svg_out = svg_in
      for (t, c) in zip(slot_colors, perm):
        svg_out = svg_out.replace(t, c)
       
      if multi_symbol:
         mss = ' '.join(multisymb_str)
         mss_nov = ' '.join(multisymb_str[:-1])
         dir_out = f'{mss_nov} {design_name} {variant}/'
         fn_out  = f'{prefix_request} {mss_nov} {design_name} {variant} {trail_str}-{p_num}.svg'      

         extended_dirout = SVG_OUTPUT_DIR+"/"+dir_out
         if not os.path.exists(extended_dirout):
           os.makedirs(extended_dirout)

         fn_out = dir_out + fn_out
      else:
         fn_out = f'{prefix_request} {name_noext} {design_name} {variant}.svg'

      with open(os.path.join(SVG_OUTPUT_DIR, fn_out), 'w') as of:
        of.write(svg_out)
      
      p_num += 1
print("All permutations have been created!")
