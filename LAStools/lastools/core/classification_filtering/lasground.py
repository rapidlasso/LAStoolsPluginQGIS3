# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasground.py
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
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasGround(LastoolsAlgorithm):
    TOOL_NAME = "LasGround"
    LASTOOL = "lasground"
    LICENSE = "c"
    LASGROUP = 4
    NO_BULGE = "NO_BULGE"
    BY_FLIGHTLINE = "BY_FLIGHTLINE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(LasGround.NO_BULGE, "no triangle bulging during TIN refinement", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasGround.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False
            )
        )
        self.addParameter(QgsProcessingParameterEnum(LasGround.TERRAIN, "terrain type", LasGround.TERRAINS, False, 2))
        self.addParameter(
            QgsProcessingParameterEnum(LasGround.GRANULARITY, "preprocessing", LasGround.GRANULARITIES, False, 1)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasGround.NO_BULGE, context):
            commands.append("-no_bulge")
        if self.parameterAsBool(parameters, LasGround.BY_FLIGHTLINE, context):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, LasGround.TERRAIN, context)
        if method != 2:
            commands.append("-" + LasGround.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, LasGround.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + LasGround.GRANULARITIES[granularity])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasGround()

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


class LasGroundPro(LastoolsAlgorithm):
    TOOL_NAME = "LasGroundPro"
    LASTOOL = "lasground"
    LICENSE = "c"
    LASGROUP = 4
    NO_BULGE = "NO_BULGE"
    BY_FLIGHTLINE = "BY_FLIGHTLINE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(LasGroundPro.NO_BULGE, "no triangle bulging during TIN refinement", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasGroundPro.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(LasGroundPro.TERRAIN, "terrain type", LasGroundPro.TERRAINS, False, 2)
        )
        self.addParameter(
            QgsProcessingParameterEnum(LasGroundPro.GRANULARITY, "preprocessing", LasGroundPro.GRANULARITIES, False, 1)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasGroundPro.NO_BULGE, context):
            commands.append("-no_bulge")
        if self.parameterAsBool(parameters, LasGroundPro.BY_FLIGHTLINE, context):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, LasGroundPro.TERRAIN, context)
        if method != 2:
            commands.append("-" + LasGroundPro.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, LasGroundPro.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + LasGroundPro.GRANULARITIES[granularity])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasGroundPro()

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
