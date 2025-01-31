"""
***************************************************************************
    lasnoise.py
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


from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasNoise(LastoolsAlgorithm):
    TOOL_NAME = "LasNoise"
    LASTOOL = "lasnoise"
    LICENSE = "c"
    LASGROUP = 3
    ISOLATED = "ISOLATED"
    STEP_XY = "STEP_XY"
    STEP_Z = "STEP_Z"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify", "remove"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ISOLATED,
                "isolated if surrounding cells have only",
                QgsProcessingParameterNumber.Integer,
                5,
                False,
                1,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP_XY,
                "resolution of isolation grid in xy",
                QgsProcessingParameterNumber.Double,
                4.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP_Z,
                "resolution of isolation grid in z",
                QgsProcessingParameterNumber.Double,
                4.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION, "what to do with isolated points", self.OPERATIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 7, False, 0, 255
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        isolated = self.parameterAsInt(parameters, self.ISOLATED, context)
        commands.append("-isolated")
        commands.append(str(isolated))
        step_xy = self.parameterAsDouble(parameters, self.STEP_XY, context)
        commands.append("-step_xy")
        commands.append(str(step_xy))
        step_z = self.parameterAsDouble(parameters, self.STEP_Z, context)
        commands.append("-step_z")
        commands.append(str(step_z))
        operation = self.parameterAsInt(parameters, self.OPERATION, context)
        if operation != 0:
            commands.append("-remove_noise")
        else:
            commands.append("-classify_as")
            classify_as = self.parameterAsInt(parameters, self.CLASSIFY_AS, context)
            commands.append(str(classify_as))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasNoise()

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


class LasNoisePro(LastoolsAlgorithm):
    TOOL_NAME = "LasNoisePro"
    LASTOOL = "lasnoise"
    LICENSE = "c"
    LASGROUP = 3
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
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ISOLATED,
                "isolated if surrounding cells have only",
                QgsProcessingParameterNumber.Integer,
                5,
                False,
                1,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP_XY,
                "resolution of isolation grid in xy",
                QgsProcessingParameterNumber.Double,
                4.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP_Z,
                "resolution of isolation grid in z",
                QgsProcessingParameterNumber.Double,
                4.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION, "what to do with isolated points", self.OPERATIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 7, False, 0, 255
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context)]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        isolated = self.parameterAsInt(parameters, self.ISOLATED, context)
        commands.append("-isolated")
        commands.append(str(isolated))
        step_xy = self.parameterAsDouble(parameters, self.STEP_XY, context)
        commands.append("-step_xy")
        commands.append(str(step_xy))
        step_z = self.parameterAsDouble(parameters, self.STEP_Z, context)
        commands.append("-step_z")
        commands.append(str(step_z))
        operation = self.parameterAsInt(parameters, self.OPERATION, context)
        if operation != 0:
            commands.append("-remove_noise")
        else:
            commands.append("-classify_as")
            classify_as = self.parameterAsInt(parameters, self.CLASSIFY_AS, context)
            commands.append(str(classify_as))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasNoisePro()

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
