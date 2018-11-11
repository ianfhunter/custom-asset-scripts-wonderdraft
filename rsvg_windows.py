# Source: https://www.cairographics.org/cookbook/librsvgpython/
#some code to give rsvg.render_cairo(ctx) ability on windows.
import os

from ctypes import *
import ctypes.util as util

def import_rsvg():
    try:
        # Present Already
        import rsvg
        return rsvg
    except (ImportError) as e:
        raise ImportError
        return None
        # if os.name == 'nt':
        #     #some workarounds for windows


        #     # l=CDLL('./bin/librsvg-2-2.dll')
        #     # l=CDLL('C:\\Users\\Ian\\Code\\custom-asset-scripts-wonderdraft\\librsvg-2-2.dll')
        #     lib = os.getcwd() + '/' +'librsvg-2-2.dll'
        #     dll = 'librsvg-2-2.dll'
        #     os.environ['PATH'] += ";C:\\Users\\Ian\\Code\\custom-asset-scripts-wonderdraft\\"
        #     os.environ['PATH'] += ";C:\\Users\\Ian\\Code\\custom-asset-scripts-wonderdraft"
        #     os.environ['PATH'] += ";librsvg-2-2.dll"
        #     os.environ['PATH'] += r";C:\\Users\\Ian\\Code\\custom-asset-scripts-wonderdraft\\"
        #     os.environ['PATH'] += r";C:\\Users\\Ian\\Code\\custom-asset-scripts-wonderdraft"
        #     os.environ['PATH'] += r";C:/Users/Ian/Code/custom-asset-scripts-wonderdraft/"
        #     os.environ['PATH'] += r";C:/Users/Ian/Code/custom-asset-scripts-wonderdraft"

        #     # dll_name = "librsvg-2-2.dll"
        #     # dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
        #     # myDll = CDLL(dllabspath)

        #     # try:
        #     #     l = windll.LoadLibrary("librsvg-2-2.dll")
        #     # except:
        #     #     print("no")

        #     # g.g_type_init()

        #     class rsvgHandle():
        #         class RsvgDimensionData(Structure):
        #             _fields_ = [("width", c_int),
        #                         ("height", c_int),
        #                         ("em",c_double),
        #                         ("ex",c_double)]

        #         class PycairoContext(Structure):
        #             _fields_ = [("PyObject_HEAD", c_byte * object.__basicsize__),
        #                         ("ctx", c_void_p),
        #                         ("base", c_void_p)]

        #         def __init__(self, path):
        #             self.path = path
        #             error = ''
        #             self.handle = l.rsvg_handle_new_from_file(self.path,error)


        #         def get_dimension_data(self):
        #             svgDim = self.RsvgDimensionData()
        #             l.rsvg_handle_get_dimensions(self.handle,byref(svgDim))
        #             return (svgDim.width,svgDim.height)

        #         def render_cairo(self, ctx):
        #             ctx.save()
        #             z = self.PycairoContext.from_address(id(ctx))
        #             l.rsvg_handle_render_cairo(self.handle, z.ctx)
        #             ctx.restore()



        #     class rsvgClass():
        #         def Handle(self,file):
        #             return rsvgHandle(file)

        #     rsvg = rsvgClass()
        #     print("rsvg emulator used.")
        #     return rsvg
        # else:
        #     print("Err: rsvg module not installed.")
        #     quit()