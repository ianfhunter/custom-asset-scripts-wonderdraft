# -*- mode: python -*-

block_cipher = None

import os, sys
execpath = sys.executable

#import site
#packages = site.getsitepackages()[0]

localAppData = os.getenv('LOCALAPPDATA')
roamingAppData = os.getenv('APPDATA')

repoFolder = os.path.dirname(os.path.abspath(os.getcwd()))

print("ROAMING FILES: ", roamingAppData)
print("LOCAL FILES: ", localAppData)
print("EXEC: ", execpath)

if True:    # if Appveyor
    libFolder = "C:\\Python36-x64\\lib"
else:
    libFolder = roamingAppData + "\\Python\\Python37"



visvis = [(libFolder + "\\site-packages\\visvis\\visvisResources", "visvisResources")]
visvis += [(libFolder + "\\site-packages\\visvis", "visvis")]
visvis += [(libFolder + "\\site-packages\\PyQt5", "PyQt5")]
visvis += [(libFolder + "\\site-packages\\pyforms_gui", "pyforms_gui")]
visvis += [(libFolder + "\\site-packages\\pyforms", "pyforms")]
visvis += [(libFolder + "\\site-packages\\confapp", "confapp")]
visvis += [("style.css", ".")]

a = Analysis(['Assetizer.py'],
             pathex=[repoFolder],
             binaries=[],
             datas=visvis,
             hiddenimports=[''],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Assetizer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
		  icon='ca_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Assetizer')

