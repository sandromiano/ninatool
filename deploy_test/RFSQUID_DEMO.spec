# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['test_loop.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas += [
('invert_representation_O30.txt', 'D:/Documents/GitHub/ninatool/ninatool/internal/mapping_functions/invert_representation_O30.txt', 'DATA'),
('series_combination_014.txt', 'D:/Documents/GitHub/ninatool/ninatool/internal/mapping_functions/series_combination_014.txt', 'DATA'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='test_loop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
