# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasground_new.py
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
from qgis.core import QgsProcessingParameterNumber, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_classification_filtering as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasGroundNew(LastoolsAlgorithm):
    TOOL_INFO = ('lasground_new', 'LasGroundNew')
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
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterEnum(
            LasGroundNew.TERRAIN, "terrain type", LasGroundNew.TERRAINS, False, 3
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasGroundNew.GRANULARITY, "preprocessing", LasGroundNew.GRANULARITIES, False, 2
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundNew.STEP, "step (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 25.0, False, 0.0, 500.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundNew.BULGE, "bulge (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 2.0, False, 0.0, 25.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundNew.SPIKE, "spike (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundNew.DOWN_SPIKE, "down spike (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundNew.OFFSET, "offset (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 0.05, False, 0.0, 1.0
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground_new")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        method = self.parameterAsInt(parameters, LasGroundNew.TERRAIN, context)
        if method == 5:
            commands.append("-step")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundNew.STEP, context)))
            commands.append("-bulge")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundNew.BULGE, context)))
            commands.append("-spike")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundNew.SPIKE, context)))
            commands.append("-spike_down")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundNew.DOWN_SPIKE, context)))
            commands.append("-offset")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundNew.OFFSET, context)))
        else:
            commands.append("-" + LasGroundNew.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, LasGroundNew.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + LasGroundNew.GRANULARITIES[granularity])
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasGroundNew()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")


class LasGroundProNew(LastoolsAlgorithm):
    TOOL_INFO = ('lasground_new', 'LasGroundProNew')
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
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterEnum(
            LasGroundProNew.TERRAIN, "terrain type", LasGroundProNew.TERRAINS, False, 3
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasGroundProNew.GRANULARITY, "preprocessing", LasGroundProNew.GRANULARITIES, False, 2
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundProNew.STEP, "step (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 25.0, False, 0.0, 500.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundProNew.BULGE, "bulge (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 2.0, False, 0.0, 25.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundProNew.SPIKE, "spike (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0
        ))
        self.addParameter(
            QgsProcessingParameterNumber(
                LasGroundProNew.DOWN_SPIKE, "down spike (for 'custom' terrain only)",
                QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0
            ))
        self.addParameter(QgsProcessingParameterNumber(
            LasGroundProNew.OFFSET, "offset (for 'custom' terrain only)",
            QgsProcessingParameterNumber.Double, 0.05, False, 0.0, 1.0
        ))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground_new")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        method = self.parameterAsInt(parameters, LasGroundProNew.TERRAIN, context)
        if method == 5:
            commands.append("-step")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundProNew.STEP, context)))
            commands.append("-bulge")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundProNew.BULGE, context)))
            commands.append("-spike")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundProNew.SPIKE, context)))
            commands.append("-spike_down")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundProNew.DOWN_SPIKE, context)))
            commands.append("-offset")
            commands.append(str(self.parameterAsDouble(parameters, LasGroundProNew.OFFSET, context)))
        else:
            commands.append("-" + LasGroundProNew.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, LasGroundProNew.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + LasGroundProNew.GRANULARITIES[granularity])
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasGroundProNew()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")
