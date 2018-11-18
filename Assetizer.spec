# -*- mode: python -*-

block_cipher = None

import os, sys
#roamingAppData = sys.executable

#import site
packages = site.getsitepackages()[0]

localAppData = os.getenv('LOCALAPPDATA')
roamingAppData = os.getenv('APPDATA')

repoFolder = os.path.dirname(os.path.abspath(os.getcwd()))

print("packages FILES: ", os.listdir(roamingAppData))
print("ROAMING FILES: ", os.listdir(roamingAppData))
print("LOCAL FILES: ", os.listdir(localAppData))

visvis = [(roamingAppData + "\\Python\\Python37\\site-packages\\visvis\\visvisResources", "visvisResources")]
visvis += [(roamingAppData + "\\Python\\Python37\\site-packages\\visvis", "visvis")]
visvis += [(roamingAppData + "\\Python\\Python37\\site-packages\\PyQt5", "PyQt5")]
visvis += [(roamingAppData + "\\Python\\Python37\\site-packages\\pyforms_gui", "pyforms_gui")]
visvis += [(roamingAppData + "\\Python\\Python37\\site-packages\\pyforms", "pyforms")]
visvis += [(roamingAppData + "\\Python\\Python37\\site-packages\\confapp", "confapp")]
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

