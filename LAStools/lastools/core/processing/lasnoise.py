# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasnoise.py
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
from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterNumber

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasNoise(LastoolsAlgorithm):
    TOOL_INFO = ('lasnoise', 'LasNoise')
    ISOLATED = "ISOLATED"
    STEP_XY = "STEP_XY"
    STEP_Z = "STEP_Z"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify", "remove"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasNoise.ISOLATED, "isolated if surrounding cells have only",
            QgsProcessingParameterNumber.Integer, 5, False, 1
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasNoise.STEP_XY, "resolution of isolation grid in xy", QgsProcessingParameterNumber.Double, 4.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasNoise.STEP_Z, "resolution of isolation grid in z", QgsProcessingParameterNumber.Double, 4.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasNoise.OPERATION, "what to do with isolated points", LasNoise.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasNoise.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 7, False, 0, 255
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasnoise")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        isolated = self.parameterAsInt(parameters, LasNoise.ISOLATED, context)
        commands.append("-isolated")
        commands.append(str(isolated))
        step_xy = self.parameterAsDouble(parameters, LasNoise.STEP_XY, context)
        commands.append("-step_xy")
        commands.append(str(step_xy))
        step_z = self.parameterAsDouble(parameters, LasNoise.STEP_Z, context)
        commands.append("-step_z")
        commands.append(str(step_z))
        operation = self.parameterAsInt(parameters, LasNoise.OPERATION, context)
        if operation != 0:
            commands.append("-remove_noise")
        else:
            commands.append("-classify_as")
            classify_as = self.parameterAsInt(parameters, LasNoise.CLASSIFY_AS, context)
            commands.append(str(classify_as))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasNoise()

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


class LasNoisePro(LastoolsAlgorithm):
    TOOL_INFO = ('lasnoise', 'LasNoisePro')
    ISOLATED = "ISOLATED"
    STEP_XY = "STEP_XY"
    STEP_Z = "STEP_Z"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify", "remove"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasNoisePro.ISOLATED, "isolated if surrounding cells have only",
            QgsProcessingParameterNumber.Integer, 5, False, 1
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasNoisePro.STEP_XY, "resolution of isolation grid in xy",
            QgsProcessingParameterNumber.Double, 4.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasNoisePro.STEP_Z, "resolution of isolation grid in z",
            QgsProcessingParameterNumber.Double, 4.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasNoisePro.OPERATION, "what to do with isolated points", LasNoisePro.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasNoisePro.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 7, False, 0, 255
        ))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasnoise")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        isolated = self.parameterAsInt(parameters, LasNoisePro.ISOLATED, context)
        commands.append("-isolated")
        commands.append(str(isolated))
        step_xy = self.parameterAsDouble(parameters, LasNoisePro.STEP_XY, context)
        commands.append("-step_xy")
        commands.append(str(step_xy))
        step_z = self.parameterAsDouble(parameters, LasNoisePro.STEP_Z, context)
        commands.append("-step_z")
        commands.append(str(step_z))
        operation = self.parameterAsInt(parameters, LasNoisePro.OPERATION, context)
        if operation != 0:
            commands.append("-remove_noise")
        else:
            commands.append("-classify_as")
            classify_as = self.parameterAsInt(parameters, LasNoisePro.CLASSIFY_AS, context)
            commands.append(str(classify_as))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasNoisePro()

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
