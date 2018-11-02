import json
import os
import platform
import re
import glob

from pathlib import Path

engine_lib = None

def getEngine(selection):
    if selection == 'CAIRO':
        return cairoRE()
    if selection == 'INKSCAPE':
        return inkscapeRE()
    if selection == 'SVGLIB':
        return svglibRE()


class RasterEngine():
    def __init__(self):
        pass

    def convert(self):
        print("no convert method present")
        raise NotImplementedError()


class cairoRE(RasterEngine):
    import cairosvg as cairo

    def convert(self, svg_path, png_path):
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)
        self.cairo.svg2png(url=svg_path, write_to=png_path)



class svglibRE(RasterEngine):

    def __init__(self):
      from svglib.svglib import svg2rlg as SVGtoIR
      from reportlab.graphics import renderPM as IRtoPNG
      global engine_lib
      engine_lib = [SVGtoIR, IRtoPNG]

    def convert(self, svg_path, png_path):
        global engine_lib
        drawing = engine_lib[0](svg_path)
        engine_lib[1].drawToFile(drawing, png_path, fmt="PNG")


class inkscapeRE(RasterEngine):
    def __init__(self):
      import subprocess as external
      global engine_lib
      engine_lib = external

    def convert(self, svg_path, png_path):
        if platform.system() == 'Windows':
        global engine_lib
            engine_lib.run([
                r'C:\Program Files\Inkscape\inkscape',
                '-z',
                svg_path,
                '-e',
                png_path
            ])


def escape_path(path):
    return str(Path(path))
