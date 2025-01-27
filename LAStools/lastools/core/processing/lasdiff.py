"""
***************************************************************************
    lasdiff.py
    ---------------------
    Date                 : May 2016 and August 2018
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

from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasDiff(LastoolsAlgorithm):
    TOOL_NAME = "LasDiff"
    LASTOOL = "lasdiff"
    LICENSE = "c"
    LASGROUP = 3
    CREATE_DIFFERENCE_FILE = "CREATE_DIFFERENCE_FILE"
    SHUTUP = "SHUTUP"
    SHUTUP_AFTER = ["5", "10", "50", "100", "1000", "10000", "50000"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("other input LAS/LAZ file", "laz", False)
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SHUTUP, "stop reporting difference after this many points", self.SHUTUP_AFTER, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CREATE_DIFFERENCE_FILE,
                "create elevation difference file (if points are in the same order)",
                False,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        shutup = self.parameterAsInt(parameters, self.SHUTUP, context)
        if shutup != 0:
            commands.append("-shutup")
            commands.append(self.SHUTUP_AFTER[shutup])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.CREATE_DIFFERENCE_FILE, context):
            self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasDiff()

    def name(self):
        return self.TOOL_NAME

    def displayName(self):
        return lastool_info[self.TOOL_NAME]["disp"]

    def group(self):
        return lasgroup_info[self.LASGROUP]["group"]

    def groupId(self):
        return lasgroup_info[self.LASGROUP]["group_id"]

    def helpUrl(self):
        return readme_url(self.LASTOOL)

    def shortHelpString(self):
        return lastool_info[self.TOOL_NAME]["help"] + help_string_help(self.LASTOOL, self.LICENSE)

    def shortDescription(self):
        return lastool_info[self.TOOL_NAME]["desc"]

    def icon(self):
        icon_file = licence[self.LICENSE]["path"]
        return QIcon(f"{paths['img']}{icon_file}")
