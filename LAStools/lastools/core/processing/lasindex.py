# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasindex.py
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

__author__ = "rapidlasso"
__date__ = "March 2024"
__copyright__ = "(C) 2024, rapidlasso GmbH"

import os
from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasIndex(LastoolsAlgorithm):
    TOOL_NAME = "LasIndex"
    LASTOOL = "lasindex"
    LICENSE = "o"
    LASGROUP = 3
    MOBILE_OR_TERRESTRIAL = "MOBILE_OR_TERRESTRIAL"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasIndex.APPEND_LAX, "append *.lax file to *.laz file", False))
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasIndex.MOBILE_OR_TERRESTRIAL, "is mobile or terrestrial LiDAR (not airborne)", False
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasIndex.APPEND_LAX, context):
            commands.append("-append")
        if self.parameterAsBool(parameters, LasIndex.MOBILE_OR_TERRESTRIAL, context):
            commands.append("-tile_size")
            commands.append("10")
            commands.append("-maximum")
            commands.append("-100")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"": None}

    def createInstance(self):
        return LasIndex()

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


class LasIndexPro(LastoolsAlgorithm):
    TOOL_NAME = "LasIndexPro"
    LASTOOL = "lasindex"
    LICENSE = "o"
    LASGROUP = 3
    MOBILE_OR_TERRESTRIAL = "MOBILE_OR_TERRESTRIAL"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(LasIndexPro.APPEND_LAX, "append *.lax file to *.laz file", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasIndexPro.MOBILE_OR_TERRESTRIAL, "is mobile or terrestrial LiDAR (not airborne)", False
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex")]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasIndexPro.APPEND_LAX, context):
            commands.append("-append")
        if self.parameterAsBool(parameters, LasIndexPro.MOBILE_OR_TERRESTRIAL, context):
            commands.append("-tile_size")
            commands.append("10")
            commands.append("-maximum")
            commands.append("-100")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"": None}

    def createInstance(self):
        return LasIndexPro()

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
