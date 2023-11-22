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

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasIndex(LastoolsAlgorithm):
    TOOL_INFO = ('lasindex', 'LasIndex')
    MOBILE_OR_TERRESTRIAL = "MOBILE_OR_TERRESTRIAL"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(
            LasIndex.APPEND_LAX, "append *.lax file to *.laz file", False
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasIndex.MOBILE_OR_TERRESTRIAL, "is mobile or terrestrial LiDAR (not airborne)", False
        ))
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasIndex.APPEND_LAX, context):
            commands.append("-append")
        if self.parameterAsBool(parameters, LasIndex.MOBILE_OR_TERRESTRIAL, context):
            commands.append("-tile_size")
            commands.append("10")
            commands.append("-maximum")
            commands.append("-100")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def createInstance(self):
        return LasIndex()

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
        img_path = 'licenced.png' \
            if descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence"] else 'open_source.png'
        return QIcon(f"{paths['img']}{img_path}")


class LasIndexPro(LastoolsAlgorithm):
    TOOL_INFO = ('lasindex', 'LasIndexPro')
    MOBILE_OR_TERRESTRIAL = "MOBILE_OR_TERRESTRIAL"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(
            LasIndexPro.APPEND_LAX, "append *.lax file to *.laz file", False
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasIndexPro.MOBILE_OR_TERRESTRIAL, "is mobile or terrestrial LiDAR (not airborne)", False
        ))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
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

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def createInstance(self):
        return LasIndexPro()

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
        img_path = 'licenced.png' \
            if descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence"] else 'open_source.png'
        return QIcon(f"{paths['img']}{img_path}")
