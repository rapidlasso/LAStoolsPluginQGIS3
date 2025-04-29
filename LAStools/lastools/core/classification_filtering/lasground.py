# -*- coding: utf-8 -*-
"""
***************************************************************************
    lasground.py
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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


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
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(self.NO_BULGE, "no triangle bulging during TIN refinement", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.TERRAIN, "terrain type", self.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(self.GRANULARITY, "preprocessing", self.GRANULARITIES, False, 1))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.NO_BULGE, context):
            commands.append("-no_bulge")
        if self.parameterAsBool(parameters, self.BY_FLIGHTLINE, context):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, self.TERRAIN, context)
        if method != 2:
            commands.append("-" + self.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, self.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + self.GRANULARITIES[granularity])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
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
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(self.NO_BULGE, "no triangle bulging during TIN refinement", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.TERRAIN, "terrain type", self.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(self.GRANULARITY, "preprocessing", self.GRANULARITIES, False, 1))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.NO_BULGE, context):
            commands.append("-no_bulge")
        if self.parameterAsBool(parameters, self.BY_FLIGHTLINE, context):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, self.TERRAIN, context)
        if method != 2:
            commands.append("-" + self.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, self.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + self.GRANULARITIES[granularity])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
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
