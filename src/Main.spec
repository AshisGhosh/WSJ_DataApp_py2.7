# -*- mode: python -*-
a = Analysis(['Main.py'],
             pathex=['C:\\Users\\Ashis\\workspace\\WSJ_DataApp_py2.7\\src'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
