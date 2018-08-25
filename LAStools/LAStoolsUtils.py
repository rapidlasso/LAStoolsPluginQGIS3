# -*- coding: utf-8 -*-

"""
***************************************************************************
    LAStoolsUtils.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : October 2014 and August 2018
    Copyright            : (C) 2014 - 2018 by Martin Isenburg
    Email                : martin near rapidlasso point com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
import subprocess

from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools.system import isWindows

class LAStoolsUtils:
 
    @staticmethod
    def hasWine():
        wine_folder = ProcessingConfig.getSetting("WINE_FOLDER")
        return (wine_folder is not None) and (wine_folder != "")

    @staticmethod
    def LAStoolsPath():
        lastools_folder = ProcessingConfig.getSetting("LASTOOLS_FOLDER")	
        if isWindows():
            wine_folder = ""
        else:
            wine_folder = ProcessingConfig.getSetting("WINE_FOLDER")
        if (wine_folder is None) or (wine_folder == ""):
            folder = lastools_folder
        else:
            folder = wine_folder + "/wine " + lastools_folder
        return folder

    @staticmethod
    def runLAStools(commands, feedback):
        commandline = " ".join(commands)
        feedback.pushConsoleInfo("LAStools command line")
        feedback.pushConsoleInfo(commandline)
        feedback.pushConsoleInfo("LAStools console output")
        output = subprocess.Popen(commandline, shell=True, stdout=subprocess.PIPE, stdin=open(os.devnull), stderr=subprocess.STDOUT, universal_newlines=False).communicate()[0]
        feedback.pushConsoleInfo(output.decode("utf-8"))
