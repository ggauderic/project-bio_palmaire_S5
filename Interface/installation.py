# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 12:04:48 2023

@author: 33649
"""
import sys
import subprocess
import pip


for package in ["winshell","pypiwin32"]:
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

import os, winshell
from win32com.client import Dispatch

desktop = winshell.desktop()
path = os.path.join(desktop, "Identificateur de Veine Palmaire.lnk")


print()
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = os.path.abspath("")+"\\Code\\launcher.vbs"
shortcut.WorkingDirectory = os.path.abspath("")+"\\Code"
shortcut.IconLocation = os.path.abspath("")+"\\Image\\ESME2.ico"
shortcut.save()
