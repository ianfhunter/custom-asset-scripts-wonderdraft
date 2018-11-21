from pyforms.basewidget import BaseWidget
from pyforms.controls   import *
from pyforms import settings as ss
from config import *
from file_system import *
import itertools
from threading import Thread
from time import sleep
from user_interface import selectEngine, initEngineSupport, getEngineSpecs
import os
import re

ss.PYFORMS_STYLESHEET = 'style.css'

from generate_svgs import generateSVGs
from generate_wonderdraft_symbols import generateWonderDraftSymbols
from convertMap import convertMap
from pyforms import start_app

from PyQt5 import QtCore, QtGui
import time


class ArgPasser:
    def __init__(self,
                 quick=False,
                 prefix="",
                 tree_mode=True,
                 max_dim=-1,
                 engine=None,
                 file=""
                 ):
        initEngineSupport(self)
        if engine is None:
            engine = selectEngine(0)
        self.engine = engine
        self.quick = quick
        self.prefix = prefix
        self.is_tree_mode = tree_mode
        self.max_dim = max_dim
        self.file = file

class ProgessTrackerThread(QtCore.QThread):

    progressPercent = QtCore.pyqtSignal(dict)

    def __init__(self, tracking_file):
        QtCore.QThread.__init__(self)
        self.tracking_file = tracking_file

    def __del__(self):
        self.wait()

    def run(self):


        progress = 0
        while progress < 100:
            sleep(0.1)
            print("Progress: ", str(progress)+"%.")
            try:
                with open(self.tracking_file) as f:
                    first_line = f.read()
                perc_found = re.findall(r"(\d+%)", first_line)[-1]
                progress = int(perc_found[:-1])
            except Exception as e:
                print(e)

            self.progressPercent.emit( {"perc": progress} )

        print("Progress: 100%. Complete.")
        self.progressPercent.emit({"perc": 100, "complete":True})

        self.finished.emit()

class mapImportGUI(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Map Maker Accellerator - City Formatter')

        #Definition of the forms fields
        self._outputmaxdim = ControlNumber('Dimension Limit', minimum=0, maximum=2048)
        self._dimdisclaimer = ControlLabel('(Not applicable for some engines)')
        self._mapfile = ControlFile('City Map File')
        self._mapdisclaimer = ControlLabel('(Must be an SVG)')

        self._engine = ControlCombo('Engine')
        initEngineSupport(ArgPasser())

        _, supported_engines, _ = getEngineSpecs()

        for i, x in enumerate(supported_engines):
            self._engine.add_item(x.name, x)

        self._progress = ControlProgress('Conversion Progress')
        self._runbutton  = ControlButton('Generate PNGs')

        self._runbutton.value = self.callFn

        #Define the organization of the Form Controls
        self._formset = [
            # '_prefix',
            ('_mapfile', '_mapdisclaimer'),
            ('_outputmaxdim', '_dimdisclaimer'),
            '_engine',
            '_progress',
            '_runbutton'
        ]

    def callFn(self):

        mdim = -1
        if (self._outputmaxdim.value > 0):
            mdim = self._outputmaxdim.value

        a = ArgPasser(
                max_dim=mdim,
                engine=self._engine.value,
                file=self._mapfile.value
            )

        thread = ProgessTrackerThread(PROGRESS_TRACKER_MAP_TMP_FILE)
        thread.progressPercent.connect(self.update_progress)
        thread.start()

        t1 = Thread(target=convertMap, args=(a, {'gui':True}))
        t1.start()


    def update_progress(self, data):
        self._progress.min = 0
        self._progress.max = 100
        self._progress.value = data["perc"]
        if "complete" in data:
            self._progress.label = "Complete"

class wonderdraftGUI(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Map Maker Accellerator - Wonderdraft PNG')

        #Definition of the forms fields
        self._prefix = ControlText('File Prefix', value="~Currently Disabled~")
        self._outputmaxdim = ControlNumber('Dimension Limit', minimum=0, maximum=2048)
        self._dimdisclaimer = ControlLabel('(Not applicable for some engines)')

        self._quickmodebox  = ControlCheckBox('Quick Mode')
        # self._engine = ControlList('Engine')
        self._engine = ControlCombo('Engine')
        initEngineSupport(ArgPasser())

        _, supported_engines, _ = getEngineSpecs()

        for i, x in enumerate(supported_engines):
            self._engine.add_item(x.name, x)

        self._mode = ControlCombo('Output Mode')
        for i, x in enumerate(["Symbol", "Tree"]):
            self._mode.add_item(x, i)

        self._progress = ControlProgress('Conversion Progress')
        self._runbutton  = ControlButton('Generate PNGs')

        self._runbutton.value = self.callFn

        #Define the organization of the Form Controls
        self._formset = [
            # '_prefix',
            ('_outputmaxdim', '_dimdisclaimer'),
            '_engine',
            '_mode',
            '_progress',
            '_runbutton'
        ]

    def callFn(self):

        mdim = -1
        if (self._outputmaxdim.value > 0):
            mdim = self._outputmaxdim.value

        a = ArgPasser(
                prefix=self._prefix.value,
                max_dim=mdim,
                engine=self._engine.value,
                tree_mode=self._mode.value == 1
            )

        thread = ProgessTrackerThread(PROGRESS_TRACKER_PNG_TMP_FILE)
        thread.progressPercent.connect(self.update_progress)
        thread.start()

        t1 = Thread(target=generateWonderDraftSymbols, args=(a, {'gui':True}))
        t1.start()


    def update_progress(self, data):
        self._progress.min = 0
        self._progress.max = 100
        self._progress.value = data["perc"]
        if "complete" in data:
            self._progress.label = "Complete"

class svgGUI(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Map Maker Accellerator - SVG Color Permuter')

        #Definition of the forms fields
        self._prefix = ControlText('File Prefix', value="")
        self._color = ControlFile('Color Scheme File')
        self._quickmodebox  = ControlCheckBox('Quick Mode (Partial Generation)')
        self._runbutton  = ControlButton('Generate SVGs')

        self._estimated_time = ControlLabel('Estimated Time: XYZmins')
        self._progress = ControlProgress('Coversion Progress')

        self._colortooltip = ControlLabel("(Blank=default)")

        self._runbutton.value = self.callFn

        #Define the organization of the Form Controls
        self._formset = [
            # '_prefix',
            '_color',
            '_quickmodebox',

            # '_estimated_time',
            '_progress',
            '_runbutton'
        ]

    def callFn(self):

        a=ArgPasser(
            prefix=self._prefix.value,
            file=self._color.value
        )

        thread = ProgessTrackerThread(PROGRESS_TRACKER_SVG_TMP_FILE)
        thread.progressPercent.connect(self.update_progress)
        thread.start()

        t1 = Thread(target=generateSVGs, args=(a, {'gui':True}))
        t1.start()


    def update_progress(self, data):
        self._progress.min = 0
        self._progress.max = 100
        self._progress.value = data["perc"]
        if "complete" in data:
            self._progress.label = "Complete"

class mainGUI(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Map Maker Accellerator - Main Window')


        self._text1 = ControlLabel('Please read the Wiki on Github for usage information. In future we try to have tooltips.', readonly=True, enabled=False)

        self._runbutton  = ControlButton('Color Scheme Applier')
        self._runbutton2  = ControlButton('SVG Conversion for Wonderdraft')
        self._runbutton3  = ControlButton('Ready City Maps for Import')

        self._text2 = ControlLabel('Potential Future Options. We encourage your feedback on what to work on next!', readonly=True, enabled=False)


        self._runbutton4  = ControlButton('Symbol Extractor', enabled=False)
        self._runbutton5  = ControlButton('Brush Convertor', enabled=False)
        self._runbutton6  = ControlButton('Color Scheme Designer', enabled=False)

        #Define the organization of the Form Controls
        self._formset = [
            '_text1',
            ('_runbutton', '_runbutton2', '_runbutton3'),
            '_text2',
            ('_runbutton4', '_runbutton5', '_runbutton6')
        ]

        self._runbutton.value = self.launchSVG
        self._runbutton2.value = self.launchPNG
        self._runbutton3.value = self.launchCity

    def launchSVG(self, btn):
        win = svgGUI()
        win.parent = self
        win.show()
    def launchPNG(self, btn):
        win = wonderdraftGUI()
        win.parent = self
        win.show()
    def launchCity(self, btn):
        win = mapImportGUI()
        win.parent = self
        win.show()


if __name__ == '__main__':

    start_app(mainGUI, geometry=(200, 200, 800, 200))
