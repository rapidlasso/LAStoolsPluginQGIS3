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

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasOverage(LastoolsAlgorithm):
    TOOL_INFO = ('lasoverage', 'LasOverage')
    CHECK_STEP = "CHECK_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify as overlap", "flag as withheld", "remove from output"]

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_horizontal_feet_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasOverage.CHECK_STEP, "size of grid used for scan angle check",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasOverage.OPERATION, "mode of operation", LasOverage.OPERATIONS, False, 0
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasoverage")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
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
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasOverage()

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


class LasOveragePro(LastoolsAlgorithm):
    TOOL_INFO = ('lasoverage', 'LasOveragePro')
    CHECK_STEP = "CHECK_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify as overlap", "flag as withheld", "remove from output"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_horizontal_feet_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasOveragePro.CHECK_STEP, "size of grid used for scan angle check",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasOveragePro.OPERATION, "mode of operation", LasOveragePro.OPERATIONS, False, 0
        ))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasoverage")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
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
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasOveragePro()

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
