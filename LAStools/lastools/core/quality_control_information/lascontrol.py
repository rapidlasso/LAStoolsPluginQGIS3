# -*- coding: utf-8 -*-
"""
***************************************************************************
    lascontrol.py
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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum, QgsProcessingParameterString
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasControl(LastoolsAlgorithm):
    TOOL_NAME = "LasControl"
    LASTOOL = "lascontrol"
    LICENSE = "c"
    LASGROUP = 6
    PARSE_STRING = "PARSE_STRING"
    USE_POINTS = "USE_POINTS"
    USE_POINTS_LIST = [
        "all",
        "ground (2)",
        "ground (2) and keypoints (8)",
        "ground (2), buldings (6), and keypoints (8)",
    ]
    ADJUST_Z = "ADJUST_Z"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("ASCII text file of control points", "csv", False)
        self.addParameter(
            QgsProcessingParameterString(
                self.PARSE_STRING, "parse string marking which columns are xyz (use 's' for skip)", "sxyz"
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.USE_POINTS, "which points to use for elevation checks", self.USE_POINTS_LIST, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ADJUST_Z, "adjust z elevation by translating away the average error", False
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-cp")
        parse = self.parameterAsString(parameters, self.PARSE_STRING, context)
        if parse != "":
            commands.append("-parse")
            commands.append(parse)
        use_point = self.parameterAsInt(parameters, self.USE_POINTS, context)
        if use_point > 0:
            commands.append("-keep_class")
            commands.append(str(2))
            if use_point > 1:
                commands.append(str(8))
                if use_point > 2:
                    commands.append(str(6))
        if self.parameterAsBool(parameters, self.ADJUST_Z, context):
            commands.append("-adjust_z")
            commands.append("-odix _adjusted")
            commands.append("-olaz")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasControl()

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
