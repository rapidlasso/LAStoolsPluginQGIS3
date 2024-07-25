# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasdiff.py
    ---------------------
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2024 by rapidlasso GmbH
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
__date__ = "March 2024"
__copyright__ = "(C) 2024, rapidlasso GmbH"

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


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
                LasDiff.SHUTUP, "stop reporting difference after this many points", LasDiff.SHUTUP_AFTER, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasDiff.CREATE_DIFFERENCE_FILE,
                "create elevation difference file (if points are in the same order)",
                False,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        shutup = self.parameterAsInt(parameters, LasDiff.SHUTUP, context)
        if shutup != 0:
            commands.append("-shutup")
            commands.append(LasDiff.SHUTUP_AFTER[shutup])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasDiff.CREATE_DIFFERENCE_FILE, context):
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
