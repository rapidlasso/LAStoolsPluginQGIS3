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
from pathlib import Path

from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools.system import isWindows


class LastoolsUtils:
    @staticmethod
    def validate_config_paths():
        wine_path, lastools_path = LastoolsUtils.lastools_path()
        if not lastools_path.exists():
            return False
        if not isWindows():
            if wine_path is None or wine_path == Path(""):
                return False
            if not wine_path.exists():
                return False
        return True

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
    def lastools_windows_path():
        lastools_folder = Path(ProcessingConfig.getSetting("LASTOOLS_FOLDER"))
        return (None, lastools_folder)

    @staticmethod
    def lastools_linux_path():
        lastools_folder = Path(ProcessingConfig.getSetting("LASTOOLS_FOLDER"))
        wine_setting = ProcessingConfig.getSetting("WINE_FOLDER")

        if wine_setting is None or wine_setting == "":
            return (None, lastools_folder)

        wine_folder = Path(wine_setting)
        return (wine_folder, lastools_folder)

    @staticmethod
    def lastools_path():
        if isWindows():
            return LastoolsUtils.lastools_windows_path()
        else:
            return LastoolsUtils.lastools_linux_path()

    @staticmethod
    def run_lastools(commands, feedback):
        if ("-gui" in commands) and ("-cpu64" in commands):
            feedback.reportError("Parameters '64 bit' and 'open LAStools GUI' can't be combined")
        if (commands[0].endswith('64.exe"') or commands[0].endswith('64"')) and "-cpu64" in commands:
            feedback.pushWarning("Parameter '64 bit' can't be combined with 64 bit executable. Removing '-cpu64'")
            commands.remove("-cpu64")
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
