# -*- coding: utf-8 -*-
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
from qgis.core import (
    Qgis,
    QgsMessageLog,
)  
from qgis.utils import iface
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools.system import isWindows

class LastoolsUtils:
    @staticmethod
    def isDebug():
        return False # todo: always set to False prio delivery

    @staticmethod
    def log(str_out):
        # output-message, output-window, messagetype
        QgsMessageLog.logMessage(str_out, "LAStools", Qgis.Info)

    @staticmethod
    def debug(str_out):
        if LastoolsUtils.isDebug():
            LastoolsUtils.log(str_out)

    @staticmethod
    def wine_folder():
        val = ProcessingConfig.getSetting("WINE_FOLDER")
        return "" if val is None else val

    @staticmethod
    def has_wine():
        return LastoolsUtils.wine_folder() != ""

    @staticmethod
    def lastools_path():
        val = ProcessingConfig.getSetting("LASTOOLS_FOLDER")
        if val is None:
            return ""
        else:
            # remove trailing path delimiter if present 
            val = os.path.normpath(val) 
            # if no "bin" ending: add
            if not val.endswith("bin"):
                # LastoolsUtils.log(f"LAStools directory [{ltp}] adjusted.")
                val = os.path.join(val, "bin")
            return val

    @staticmethod
    def lastools_check_path():
        # check config path on plugin load and report problems to the main notification
        err = ""
        ltp = LastoolsUtils.lastools_path()
        LastoolsUtils.debug(f"path={ltp}")
        if ltp == "":
            err = "No LAStools directory configured."
        if not os.path.isdir(ltp):
            err = f"LAStools directory [{ltp}] not found."
        # report
        if err != "":
            # show in main window message bar
            iface.messageBar().pushMessage("Error", ": " + err + " Please check LAStool plugin configuration.", level=Qgis.Critical)            
        return

    @staticmethod
    def execute_command(commandline: str):
        sub = subprocess.Popen(
            commandline,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=False,
        )
        output = sub.communicate()[0]
        sub.kill()
        out = ""
        if isWindows():
            out = output.decode("cp850", errors="replace")
        else:
            out = output.decode("utf-8", errors="replace")
        return sub.returncode, out
