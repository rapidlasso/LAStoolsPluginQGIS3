"""
***************************************************************************
    utils.py
    ---------------------
    Date                 : January 2025
    Copyright            : (c) 2025 by rapidlasso GmbH
    Email                : info near rapidlasso point de
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = "rapidlasso"
__date__ = "January 2025"
__copyright__ = "(c) 2025, rapidlasso GmbH"

import os
import subprocess

from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools.system import isWindows


class LastoolsUtils:
    @staticmethod
    def has_wine():
        wine_folder = ProcessingConfig.getSetting("WINE_FOLDER")
        return (wine_folder is not None) and (wine_folder != "")

    @staticmethod
    def command_ext():
        if LastoolsUtils.has_wine():
            return ".exe"
        else:
            return ""

    @staticmethod
    def lastools_path():
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
    def run_lastools(commands, feedback):
        if ("-gui" in commands) and ("-cpu64" in commands):
            feedback.reportError("Parameters '64 bit' and 'open LAStools GUI' can't be combined")
        commandline = " ".join(commands)
        feedback.pushConsoleInfo("LAStools command line")
        feedback.pushConsoleInfo(commandline)
        feedback.pushConsoleInfo("LAStools console output")
        output = subprocess.Popen(
            commandline,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=False,
        ).communicate()[0]
        feedback.pushConsoleInfo(output.decode("utf-8"))
