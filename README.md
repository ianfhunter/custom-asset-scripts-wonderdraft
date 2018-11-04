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

You can install using requirements.txt and pip3

For the imagemagick engine (windows), download here http://www.imagemagick.org/script/download.php#windows

### Switching Render Engines
change RENDER_ENGINE variable to the appropiate one
you may also like to change PATH_TO_IMAGEMAGICK & PATH_TO_INKSCAPE if they do not match up.

See the Wiki for more info
