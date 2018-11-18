# -*- mode: python -*-

block_cipher = None


visvis = [("C:\\Users\\ihunter\\AppData\\Roaming\\Python\\Python37\\site-packages\\visvis\\visvisResources", "visvisResources")]
visvis += [("C:\\Users\\ihunter\\AppData\\Roaming\\Python\\Python37\\site-packages\\visvis", "visvis")]
visvis += [("C:\\Users\\ihunter\\AppData\\Roaming\\Python\\Python37\\site-packages\\PyQt5", "PyQt5")]
visvis += [("C:\\Users\\ihunter\\AppData\\Roaming\\Python\\Python37\\site-packages\\pyforms_gui", "pyforms_gui")]
visvis += [("C:\\Users\\ihunter\\AppData\\Roaming\\Python\\Python37\\site-packages\\pyforms", "pyforms")]
visvis += [("C:\\Users\\ihunter\\AppData\\Roaming\\Python\\Python37\\site-packages\\confapp", "confapp")]
visvis += [("style.css", ".")]

# 'C:\\Users\\ihunter\\AppData\\Roaming\\Python\\Python37\\site-packages\\visvis\\'
a = Analysis(['Assetizer.py'],
             pathex=['C:\\Users\\ihunter\\Documents\\GitHub\\custom-asset-scripts-wonderdraft'],
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

			   		 