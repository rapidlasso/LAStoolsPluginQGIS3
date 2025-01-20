# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassortpy
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

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterFile, QgsProcessingParameterBoolean

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasSort(LastoolsAlgorithm):
    TOOL_NAME = "LasSort"
    LASTOOL = "lassort"
    LICENSE = "c"
    LASGROUP = 3
    BY_GPS_TIME = "BY_GPS_TIME"
    BY_RETURN_NUMBER = "BY_RETURN_NUMBER"
    BY_POINT_SOURCE_ID = "BY_POINT_SOURCE_ID"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(self.BY_GPS_TIME, "sort by GPS time", False))
        self.addParameter(QgsProcessingParameterBoolean(self.BY_RETURN_NUMBER, "sort by return number", False))
        self.addParameter(QgsProcessingParameterBoolean(self.BY_POINT_SOURCE_ID, "sort by point source ID", False))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.BY_GPS_TIME, context):
            commands.append("-gps_time")
        if self.parameterAsBool(parameters, self.BY_RETURN_NUMBER, context):
            commands.append("-return_number")
        if self.parameterAsBool(parameters, self.BY_POINT_SOURCE_ID, context):
            commands.append("-point_source")
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

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

    def createInstance(self):
        return LasSort()


class LasSortPro(LastoolsAlgorithm):
    TOOL_NAME = "LasSortPro"
    LASTOOL = "lassort"
    LICENSE = "c"
    LASGROUP = 3
    BY_GPS_TIME = "BY_GPS_TIME"
    BY_RETURN_NUMBER = "BY_RETURN_NUMBER"
    BY_POINT_SOURCE_ID = "BY_POINT_SOURCE_ID"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(self.BY_GPS_TIME, "sort by GPS time", False))
        self.addParameter(QgsProcessingParameterBoolean(self.BY_RETURN_NUMBER, "sort by return number", False))
        self.addParameter(QgsProcessingParameterBoolean(self.BY_POINT_SOURCE_ID, "sort by point source ID", False))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.BY_GPS_TIME, context):
            commands.append("-gps_time")
        if self.parameterAsBool(parameters, self.BY_RETURN_NUMBER, context):
            commands.append("-return_number")
        if self.parameterAsBool(parameters, self.BY_POINT_SOURCE_ID, context):
            commands.append("-point_source")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"": None}

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

    def createInstance(self):
        return LasSortPro()
