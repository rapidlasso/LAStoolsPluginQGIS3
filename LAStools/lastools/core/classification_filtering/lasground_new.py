# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasground_new.py
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
from qgis.core import QgsProcessingParameterNumber, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasGroundNew(LastoolsAlgorithm):
    TOOL_NAME = "LasGroundNew"
    LASTOOL = "lasground_new"
    LICENSE = "c"
    LASGROUP = 4
    TERRAIN = "TERRAIN"
    TERRAINS = ["wilderness", "nature", "town", "city", "metro", "custom"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine", "hyper_fine"]
    STEP = "STEP"
    BULGE = "BULGE"
    SPIKE = "SPIKE"
    DOWN_SPIKE = "DOWN_SPIKE"
    OFFSET = "OFFSET"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterEnum(self.TERRAIN, "terrain type", self.TERRAINS, False, 3))
        self.addParameter(QgsProcessingParameterEnum(self.GRANULARITY, "preprocessing", self.GRANULARITIES, False, 2))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP,
                "step (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
                500.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.BULGE,
                "bulge (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                2.0,
                False,
                0.0,
                25.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SPIKE,
                "spike (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
                25.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DOWN_SPIKE,
                "down spike (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
                25.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.OFFSET,
                "offset (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                0.05,
                False,
                0.0,
                1.0,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        method = self.parameterAsInt(parameters, self.TERRAIN, context)
        if method == 5:
            commands.append("-step")
            commands.append(str(self.parameterAsDouble(parameters, self.STEP, context)))
            commands.append("-bulge")
            commands.append(str(self.parameterAsDouble(parameters, self.BULGE, context)))
            commands.append("-spike")
            commands.append(str(self.parameterAsDouble(parameters, self.SPIKE, context)))
            commands.append("-spike_down")
            commands.append(str(self.parameterAsDouble(parameters, self.DOWN_SPIKE, context)))
            commands.append("-offset")
            commands.append(str(self.parameterAsDouble(parameters, self.OFFSET, context)))
        else:
            commands.append("-" + self.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, self.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + self.GRANULARITIES[granularity])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasGroundNew()

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


class LasGroundProNew(LastoolsAlgorithm):
    TOOL_NAME = "LasGroundProNew"
    LASTOOL = "lasground_new"
    LICENSE = "c"
    LASGROUP = 4
    TERRAIN = "TERRAIN"
    TERRAINS = ["wilderness", "nature", "town", "city", "metro", "custom"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine", "hyper_fine"]
    STEP = "STEP"
    BULGE = "BULGE"
    SPIKE = "SPIKE"
    DOWN_SPIKE = "DOWN_SPIKE"
    OFFSET = "OFFSET"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterEnum(self.TERRAIN, "terrain type", self.TERRAINS, False, 3))
        self.addParameter(QgsProcessingParameterEnum(self.GRANULARITY, "preprocessing", self.GRANULARITIES, False, 2))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP,
                "step (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
                500.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.BULGE,
                "bulge (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                2.0,
                False,
                0.0,
                25.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SPIKE,
                "spike (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
                25.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DOWN_SPIKE,
                "down spike (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
                25.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.OFFSET,
                "offset (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double,
                0.05,
                False,
                0.0,
                1.0,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        method = self.parameterAsInt(parameters, self.TERRAIN, context)
        if method == 5:
            commands.append("-step")
            commands.append(str(self.parameterAsDouble(parameters, self.STEP, context)))
            commands.append("-bulge")
            commands.append(str(self.parameterAsDouble(parameters, self.BULGE, context)))
            commands.append("-spike")
            commands.append(str(self.parameterAsDouble(parameters, self.SPIKE, context)))
            commands.append("-spike_down")
            commands.append(str(self.parameterAsDouble(parameters, self.DOWN_SPIKE, context)))
            commands.append("-offset")
            commands.append(str(self.parameterAsDouble(parameters, self.OFFSET, context)))
        else:
            commands.append("-" + self.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, self.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + self.GRANULARITIES[granularity])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasGroundProNew()

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
