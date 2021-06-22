# -*- mode: python ; coding: utf-8 -*-

import shutil
block_cipher = None


a = Analysis(['tasmohab.py'],
             pathex=['C:\\Users\\user\\Documents\\PyCharm\\venv\\Lib\\site-packages', 'C:\\Users\\user\\Documents\\PyCharm\\TasmoHAB', 'C:\\Users\\user\\Documents\\PyCharm\\TasmoHAB\\ohgen', 'C:\\Users\\user\\Documents\\PyCharm\\TasmoHAB'],
             binaries=[],
             datas=[('ohgen/templates/*', 'ohgen/templates'),('icon.ico', '.')],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='tasmohab',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon.ico')

#### Gifford47 #####
if os.path.exists('{0}/ohgen/templates'.format(DISTPATH)):
    shutil.rmtree('{0}/ohgen/templates'.format(DISTPATH))
shutil.copytree('ohgen/templates', '{0}/ohgen/templates'.format(DISTPATH))                 # only for one-file option
shutil.copy('ohgen/template.yaml', '{0}'.format(DISTPATH))                 # only for one-file option
