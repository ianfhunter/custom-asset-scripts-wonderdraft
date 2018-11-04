import json
import os
import platform
import re
import glob

from pathlib import Path

engine_lib = None

PATH_TO_IMAGEMAGICK = r'C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe'
PATH_TO_INKSCAPE = r'C:\Program Files\Inkscape\inkscape.com'

def getEngine(selection, args):
    if selection == 'CAIRO':
        return cairoRE()
    if selection == 'CAIROSVG':
        return cairoSVGRE()
    if selection == 'INKSCAPE':
        return inkscapeRE()
    if selection == 'SVGLIB':
        return svglibRE()
    if selection == 'IMAGEMAGICK':
        return imageMagickRE(args.max_dim)


class RasterEngine():
    def __init__(self):
        pass

    def convert(self, svg_path, png_path):
        # print(svg_path , "->", png_path)
        pass

class cairoSVGRE(RasterEngine):
    def __init__(self):
        import cairosvg as cairo
        global engine_lib
        engine_lib = cairo

    def convert(self, svg_path, png_path):
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)
        engine_lib.svg2png(url=svg_path, write_to=png_path)


class imageMagickRE(RasterEngine):
    def __init__(self, max_dim):
      import subprocess as external
      global engine_lib
      engine_lib = external #Image
      self.max_dim = str(max_dim)

    def convert(self, svg_path, png_path):
        global engine_lib

        super(imageMagickRE, self).convert(svg_path, png_path)
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)

            if self.max_dim == "-1":
                proc = engine_lib.run([
                    PATH_TO_IMAGEMAGICK,
                    '-background', 'none',
                    svg_path,
                    png_path,
                ])
            else:
                proc = engine_lib.run([
                    PATH_TO_IMAGEMAGICK,
                    '-background', 'none',
                    svg_path,
                    '-resize', self.max_dim + 'x' + self.max_dim,
                    png_path,
                ])


# "C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe" "C:\Users\Ian\Code\custom-asset-scripts-wonderdraft\svg_output\Flat Design Trees Master Autumn A\ Flat Design Trees Master Autumn A 1a1-1.svg" a.png

class cairoRE(RasterEngine):
    def __init__(self):
        import cairo as cairo
        from rsvg_windows import import_rsvg
        rsvg = import_rsvg()
        global engine_lib
        engine_lib = [cairo, rsvg]

    def convert(self, svg_path, png_path):
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)

        # file = open(svg_path, "r")
        # for line in file:
        #     if re.search("width=", line):
        #         print (line)
        #     if re.search("height=", line):
        #         print (line)

        width, height = 256, 256    # BAD DEFAULT
        print("Warning: using default size of 256x256")
        img = engine_lib[0].ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        ctx = engine_lib[0].Context(img)
        handler = engine_lib[1].Handle(svg_path)
        handler.render_cairo(ctx)
        img.write_to_png(png_path)



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
        global engine_lib
        super(inkscapeRE, self).convert(svg_path, png_path)
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)
            engine_lib.run([
                PATH_TO_INKSCAPE,
                '--without-gui',
                svg_path,
                '--export-png='+png_path
            ])


def splitPath(path):
    if platform.system() == 'Windows':
        return path.split("\\")[-1]
    else:
        return path.split("/")[-1]


def escape_path(path):
    return str(Path(path))
