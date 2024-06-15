# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['Mainwindow.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\User\\OneDrive\\Desktop\\GitExercise\\GitExercise-TT1L-04\\Icons\\fillicon.png', 'Icons'),
        ('C:\\Users\\User\\OneDrive\\Desktop\\GitExercise\\GitExercise-TT1L-04\\Icons\\redoicon.png', 'Icons'),
        ('C:\\Users\\User\\OneDrive\\Desktop\\GitExercise\\GitExercise-TT1L-04\\Icons\\undoicon.png', 'Icons'),
        ('C:\\Users\\User\\OneDrive\\Desktop\\GitExercise\\GitExercise-TT1L-04\\Icons\\brushicon.png', 'Icons'),
        ('C:\\Users\\User\\OneDrive\\Desktop\\GitExercise\\GitExercise-TT1L-04\\Icons\\erasericon.png', 'Icons')
        ('C:\\Users\\User\\OneDrive\\Desktop\\GitExercise\\GitExercise-TT1L-04\\Icons\\sidebarbg.jpg', 'Icons')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Mainwindow',
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
