# PyInstaller spec for the Subtitles Translator CLI.
# Build with: pyinstaller subtitles-translator.spec
# Produces a single self-contained binary in dist/ for the host platform.

a = Analysis(
    ["src/app/__main__.py"],
    pathex=["src"],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="subtitles-translator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
