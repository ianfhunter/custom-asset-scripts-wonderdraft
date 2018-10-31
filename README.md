# Accelerated Assets for Wonderdraft
Scripts to accelerate Asset creation for the map making tool Wonderdraft

Two scripts currently exist:

#### Generate SVGS

This script generates different SVGs based on an original and some given color schemes.
Outputs in 'svg_output'

Tip: Define your own Custom color schemes in color_schemes.txt
Colors must be defined using Hexadecimal Format.

#### Generate WonderDraft Symbols

This script generates trees or symbols for Wonderdraft from the svgs produced with the previous script.
Outputs in 'trees' or 'symbols' accordingly.

### Installation

#### Windows
* Install Python3 (https://www.python.org/downloads/windows/)
* Install svglib through pip3. 
  * You will need to specify svglib==0.9.0b to get the right version