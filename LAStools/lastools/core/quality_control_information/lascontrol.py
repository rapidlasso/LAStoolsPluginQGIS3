# -*- coding: utf-8 -*-

"""
***************************************************************************
    lascontrol.py
    ---------------------
    Date                 : November 2023
    Copyright            : (C) 2023 by rapidlasso GmbH
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

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterString, QgsProcessingParameterBoolean, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_quality_control_information as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasControl(LastoolsAlgorithm):
    TOOL_INFO = ('lascontrol', 'LasControl')
    PARSE_STRING = "PARSE_STRING"
    USE_POINTS = "USE_POINTS"
    USE_POINTS_LIST = ["all", "ground (2)", "ground (2) and keypoints (8)",
                       "ground (2), buldings (6), and keypoints (8)"]
    ADJUST_Z = "ADJUST_Z"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui()
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui(
            "ASCII text file of control points", "csv", False
        )
        self.addParameter(QgsProcessingParameterString(
            LasControl.PARSE_STRING, "parse string marking which columns are xyz (use 's' for skip)", "sxyz"
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasControl.USE_POINTS, "which points to use for elevation checks", LasControl.USE_POINTS_LIST, False, 0
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasControl.ADJUST_Z, "adjust z elevation by translating away the average error", False
        ))
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lascontrol")]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-cp")
        parse = self.parameterAsString(parameters, LasControl.PARSE_STRING, context)
        if parse != "":
            commands.append("-parse")
            commands.append(parse)
        use_point = self.parameterAsInt(parameters, LasControl.USE_POINTS, context)
        if use_point > 0:
            commands.append("-keep_class")
            commands.append(str(2))
            if use_point > 1:
                commands.append(str(8))
                if use_point > 2:
                    commands.append(str(6))
        if self.parameterAsBool(parameters, LasControl.ADJUST_Z, context):
            commands.append("-adjust_z")
            commands.append("-odix _adjusted")
            commands.append("-olaz")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasControl()

    def name(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["name"]

    def displayName(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["display_name"]

    def group(self):
        return descript_info["info"]["group"]

    def groupId(self):
        return descript_info["info"]["group_id"]

    def helpUrl(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["url_path"]

    def shortHelpString(self):
        return self.tr(descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_help_string"])

    def shortDescription(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_description"]

    def icon(self):
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")
