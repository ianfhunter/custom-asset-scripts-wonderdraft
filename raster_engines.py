import json
import os
import platform
import re
import glob

from pathlib import Path

PATH_TO_IMAGEMAGICK = r'C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe'
PATH_TO_INKSCAPE = r'C:\Program Files\Inkscape\inkscape.com'

def getEngine2(args):

    possible_engines = [
        cairoSVGRE(),
        imageMagickRE(),
        inkscapeRE(),
        cairoRE(),
        svglibRE(),
        rsvgRE()
    ]

    supported_engines = []
    unsupported_engines = []

    for e in possible_engines:
        try:
            e.load(args)
            supported_engines.append(e.name)
        except:
            unsupported_engines.append(e.name)

    print("Inactive Rasterizing Engines: ")
    for x in unsupported_engines:
        print("*", x)


    print("Available Rasterizing Engines: ")
    for x in range(len(supported_engines)):
        print("("+str(x)+")", supported_engines[x])

    print("Please Select an engine:")


def getEngine(selection, args):
    if selection == 'CAIRO':
        a = cairoRE()
    if selection == 'CAIROSVG':
        a = cairoSVGRE()
    if selection == 'INKSCAPE':
        a = inkscapeRE()
    if selection == 'SVGLIB':
        a = svglibRE()
    if selection == 'IMAGEMAGICK':
        a = imageMagickRE()
    if selection == 'RSVG':
        a = rsvgRE()

    a.load(args)
    return a


class RasterEngine():
    def __init__(self):
        pass

    def convert(self, svg_path, png_path):
        # print(svg_path , "->", png_path)
        pass

class cairoSVGRE(RasterEngine):
    def __init__(self):
        self.name = "CairoSVG"

    def load(self, args):
        import cairosvg as cairo
        self.engine_lib = cairo

    def convert(self, svg_path, png_path):
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)
        self.engine_lib.svg2png(url=svg_path, write_to=png_path)


class imageMagickRE(RasterEngine):
    def __init__(self):
        self.name = "ImageMagick"

    def load(self, args):
        import subprocess as external
        self.engine_lib = external
        self.max_dim = str(args.max_dim)
        if not os.path.isdir(PATH_TO_IMAGEMAGICK):
            raise Exception

    def convert(self, svg_path, png_path):

        super(imageMagickRE, self).convert(svg_path, png_path)
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)

            if self.max_dim == "-1":
                proc = self.engine_lib.run([
                    PATH_TO_IMAGEMAGICK,
                    '-background', 'none',
                    svg_path,
                    png_path,
                ])
            else:
                proc = self.engine_lib.run([
                    PATH_TO_IMAGEMAGICK,
                    '-background', 'none',
                    svg_path,
                    '-resize', self.max_dim + 'x' + self.max_dim,
                    png_path,
                ])

class cairoRE(RasterEngine):    # Incomplete
    def __init__(self):
        self.name = "Cairo RSVG"

    def load(self, args):
        import cairo as cairo
        from rsvg_windows import import_rsvg
        rsvg = import_rsvg()
        self.engine_lib = [cairo, rsvg]

    def convert(self, svg_path, png_path):
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)

        width, height = 256, 256    # BAD DEFAULT
        print("Warning: using default size of 256x256")
        img = self.engine_lib[0].ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        ctx = self.engine_lib[0].Context(img)
        handler = self.engine_lib[1].Handle(svg_path)
        handler.render_cairo(ctx)
        img.write_to_png(png_path)


class svglibRE(RasterEngine):

    def __init__(self):
        self.name = "svgLib"

    def load(self, args):
        from svglib.svglib import svg2rlg as SVGtoIR
        from reportlab.graphics import renderPM as IRtoPNG
        self.engine_lib = [SVGtoIR, IRtoPNG]

    def convert(self, svg_path, png_path):
        drawing = self.engine_lib[0](svg_path)
        self.engine_lib[1].drawToFile(drawing, png_path, fmt="PNG")


class rsvgRE(RasterEngine):

    def __init__(self):
        self.name = "rsvg"

    def load(self, args):
        import subprocess as external
        self.engine_lib = external

    def convert(self, svg_path, png_path):
        # os.system(
        self.engine_lib.run([
            'rsvg-convert',
            svg_path,
            '--output',
            png_path
        ])



class inkscapeRE(RasterEngine):
    def __init__(self):
        self.name = "InkScape"

    def load(self, args):
        import subprocess as external
        self.engine_lib = external
        if not os.path.isdir(PATH_TO_INKSCAPE):
            raise Exception

    def convert(self, svg_path, png_path):
        super(inkscapeRE, self).convert(svg_path, png_path)
        if platform.system() == 'Windows':
            png_path = escape_path(png_path)
            svg_path = escape_path(svg_path)
            self.engine_lib.run([
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
