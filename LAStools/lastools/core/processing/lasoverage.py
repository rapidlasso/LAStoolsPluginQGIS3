# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoverage.py
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
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasOverage(LastoolsAlgorithm):
    TOOL_NAME = "LasOverage"
    LASTOOL = "lasoverage"
    LICENSE = "c"
    LASGROUP = 3
    CHECK_STEP = "CHECK_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify as overlap", "flag as withheld", "remove from output"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_horizontal_feet_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                LasOverage.CHECK_STEP,
                "size of grid used for scan angle check",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(LasOverage.OPERATION, "mode of operation", LasOverage.OPERATIONS, False, 0)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasoverage")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_horizontal_feet_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, LasOverage.CHECK_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, LasOverage.OPERATION, context)
        if operation == 1:
            commands.append("-flag_as_withheld")
        elif operation == 2:
            commands.append("-remove_overage")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasOverage()

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


class LasOveragePro(LastoolsAlgorithm):
    TOOL_NAME = "LasOveragePro"
    LASTOOL = "lasoverage"
    LICENSE = "c"
    LASGROUP = 3
    CHECK_STEP = "CHECK_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify as overlap", "flag as withheld", "remove from output"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_horizontal_feet_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                LasOveragePro.CHECK_STEP,
                "size of grid used for scan angle check",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(LasOveragePro.OPERATION, "mode of operation", LasOveragePro.OPERATIONS, False, 0)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasoverage")]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_horizontal_feet_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, LasOveragePro.CHECK_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, LasOveragePro.OPERATION, context)
        if operation == 1:
            commands.append("-flag_as_withheld")
        elif operation == 2:
            commands.append("-remove_overage")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasOveragePro()

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
