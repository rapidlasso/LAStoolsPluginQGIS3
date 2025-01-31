"""
***************************************************************************
    lasreturn.py
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

from qgis.core import QgsProcessingParameterBoolean
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasReturn(LastoolsAlgorithm):
    TOOL_NAME = "LasReturn"
    LASTOOL = "lasreturn"
    LICENSE = "c"
    LASGROUP = 6

    CHECK_RETURN_NUMBERING = "CHECK_RETURN_NUMBERING"
    COMPUTE_GAP_TO_NEXT_RETURN = "COMPUTE_GAP_TO_NEXT_RETURN"
    REPAIR_NUMBER_OF_RETURNS = "REPAIR_NUMBER_OF_RETURNS"
    SKIP_INCOMPLETE = "SKIP_INCOMPLETE"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()

        self.addParameter(
            QgsProcessingParameterBoolean(self.CHECK_RETURN_NUMBERING, "print histogram about returns", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.COMPUTE_GAP_TO_NEXT_RETURN, "adds attribute 'gap to next return'", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.REPAIR_NUMBER_OF_RETURNS, "repair invalid number of returns", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.SKIP_INCOMPLETE, "skip incomplete returns", False))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.CHECK_RETURN_NUMBERING, context):
            commands.append("-check_return_numbering")
        if self.parameterAsBool(parameters, self.COMPUTE_GAP_TO_NEXT_RETURN, context):
            commands.append("-compute_gap_to_next_return")
        if self.parameterAsBool(parameters, self.REPAIR_NUMBER_OF_RETURNS, context):
            commands.append("-repair_number_of_returns")
        if self.parameterAsBool(parameters, self.SKIP_INCOMPLETE, context):
            commands.append("-skip_incomplete")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasReturn()

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


class LasReturnPro(LastoolsAlgorithm):
    TOOL_NAME = "LasReturnPro"
    LASTOOL = "lasreturn"
    LICENSE = "c"
    LASGROUP = 6

    CHECK_RETURN_NUMBERING = "CHECK_RETURN_NUMBERING"
    COMPUTE_GAP_TO_NEXT_RETURN = "COMPUTE_GAP_TO_NEXT_RETURN"
    REPAIR_NUMBER_OF_RETURNS = "REPAIR_NUMBER_OF_RETURNS"
    SKIP_INCOMPLETE = "SKIP_INCOMPLETE"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(self.CHECK_RETURN_NUMBERING, "print histogram about returns", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.COMPUTE_GAP_TO_NEXT_RETURN, "adds attribute 'gap to next return'", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.REPAIR_NUMBER_OF_RETURNS, "repair invalid number of returns", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.SKIP_INCOMPLETE, "skip incomplete returns", False))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_output_directory_gui()

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
        if self.parameterAsBool(parameters, self.CHECK_RETURN_NUMBERING, context):
            commands.append("-check_return_numbering")
        if self.parameterAsBool(parameters, self.COMPUTE_GAP_TO_NEXT_RETURN, context):
            commands.append("-compute_gap_to_next_return")
        if self.parameterAsBool(parameters, self.REPAIR_NUMBER_OF_RETURNS, context):
            commands.append("-repair_number_of_returns")
        if self.parameterAsBool(parameters, self.SKIP_INCOMPLETE, context):
            commands.append("-skip_incomplete")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasReturnPro()

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
