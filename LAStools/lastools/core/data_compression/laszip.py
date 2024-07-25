# -*- coding: utf-8 -*-

"""
***************************************************************************
    laszip.py
    ---------------------
    Date                 : November 2023
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
from qgis.core import QgsProcessingParameterBoolean

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasZip(LastoolsAlgorithm):
    TOOL_NAME = "LasZip"
    LASTOOL = "laszip"
    LICENSE = "o"
    LASGROUP = 1
    REPORT_SIZE = "REPORT_SIZE"
    CREATE_LAX = "CREATE_LAX"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasZip.REPORT_SIZE, "only report size", False))
        self.addParameter(
            QgsProcessingParameterBoolean(LasZip.CREATE_LAX, "create spatial indexing file (*.lax)", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(LasZip.APPEND_LAX, "append *.lax into *.laz file", False))
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasZip.REPORT_SIZE, context):
            commands.append("-size")
        if self.parameterAsBool(parameters, LasZip.CREATE_LAX, context):
            commands.append("-lax")
        if self.parameterAsBool(parameters, LasZip.APPEND_LAX, context):
            commands.append("-append")
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasZip()

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


class LasZipPro(LastoolsAlgorithm):
    TOOL_NAME = "LasZipPro"
    LASTOOL = "laszip"
    LICENSE = "o"
    LASGROUP = 1
    REPORT_SIZE = "REPORT_SIZE"
    CREATE_LAX = "CREATE_LAX"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_point_output_format_gui(1)
        self.add_parameters_output_appendix_gui()
        self.add_parameters_additional_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasZipPro.REPORT_SIZE, "only report size", False))
        self.addParameter(
            QgsProcessingParameterBoolean(LasZipPro.CREATE_LAX, "create spatial indexing file (*.lax)", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(LasZipPro.APPEND_LAX, "append *.lax into *.laz file", False))
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasZipPro.REPORT_SIZE, context):
            commands.append("-size")
        if self.parameterAsBool(parameters, LasZipPro.CREATE_LAX, context):
            commands.append("-lax")
        if self.parameterAsBool(parameters, LasZipPro.APPEND_LAX, context):
            commands.append("-append")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasZipPro()

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
