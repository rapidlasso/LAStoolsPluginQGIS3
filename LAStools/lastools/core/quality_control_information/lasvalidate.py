# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasvalidate.py
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


class LasValidate(LastoolsAlgorithm):
    TOOL_NAME = "LasValidate"
    LASTOOL = "lasvalidate"
    LICENSE = "f"
    LASGROUP = 6
    ONE_REPORT_PER_FILE = "ONE_REPORT_PER_FILE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(LasValidate.ONE_REPORT_PER_FILE, "save report to '*_LVS.xml'", False)
        )
        self.add_parameters_generic_output_gui("Output XML file", "xml", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasValidate.ONE_REPORT_PER_FILE, context):
            commands.append("-oxml")
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasValidate()

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


class LasValidatePro(LastoolsAlgorithm):
    TOOL_NAME = "LasValidatePro"
    LASTOOL = "lasvalidate"
    LICENSE = "f"
    LASGROUP = 6
    ONE_REPORT_PER_FILE = "ONE_REPORT_PER_FILE"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(LasValidatePro.ONE_REPORT_PER_FILE, "save report to '*_LVS.xml'", False)
        )
        self.add_parameters_generic_output_gui("Output XML file", "xml", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasValidatePro.ONE_REPORT_PER_FILE, context):
            commands.append("-oxml")
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasValidatePro()

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
