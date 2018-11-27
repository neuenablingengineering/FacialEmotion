# coding=gbk
import sys
import numpy
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'packages': ['numpy'],'includes' :['cv2', 'numpy.core.multiarray'], 'excludes': [],"packages"  : ["os"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

iconpath = "Ico\logo.ico"

setup(  name = 'main',
        version = '0.01',
        options = {'build_exe': build_exe_options},
        executables = [Executable('main.py', base=base, icon=iconpath)])



