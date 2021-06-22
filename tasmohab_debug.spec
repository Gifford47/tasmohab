# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['tasmohab.py'],
             pathex=['C:\\Users\\user\\Documents\\PyCharm\\venv\\Lib\\site-packages', 'C:\\Users\\user\\Documents\\PyCharm\\TasmoHAB', 'C:\\Users\\user\\Documents\\PyCharm\\TasmoHAB\\ohgen', 'C:\\Users\\user\\Documents\\PyCharm\\TasmoHAB'],
             binaries=[],
             datas=[('ohgen/templates/*', 'ohgen/templates')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [('v', None, 'OPTION')],
          exclude_binaries=True,
          name='tasmohab',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='tasmohab_debug')
