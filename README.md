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

### Performance

Some performance numbers based on symbol mode.

#### Linux

| Raster Engine | Sample Time |
| ------------- | -------------: |
| `CAIROSVG`  | 22s  |
| `SVGLIB`  | 2m44s  |

#### Windows

| Raster Engine | Sample Time |
| ------------- | -------------: |
| `INKSCAPE`  | 12m19s  |
| `IMAGEMAGICK`  | 1m28s  |
| `SVGLIB`  | 1m50s  |