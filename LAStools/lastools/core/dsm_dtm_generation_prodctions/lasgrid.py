# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgrid.py
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
from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterBoolean

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasGrid(LastoolsAlgorithm):
    TOOL_NAME = "LasGrid"
    LASTOOL = "lasgrid"
    LICENSE = "c"
    LASGROUP = 5
    ATTRIBUTE = "ATTRIBUTE"
    METHOD = "METHOD"
    ATTRIBUTES = ["elevation", "intensity", "rgb", "classification"]
    METHODS = ["lowest", "highest", "average", "stddev"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_step_gui()
        self.addParameter(QgsProcessingParameterEnum(LasGrid.ATTRIBUTE, "attribute", LasGrid.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasGrid.METHOD, "method", LasGrid.METHODS, False, 0))
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasGrid.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_raster_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_step_commands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, LasGrid.ATTRIBUTE, context)
        if attribute != 0:
            commands.append("-" + LasGrid.ATTRIBUTES[attribute])
        method = self.parameterAsInt(parameters, LasGrid.METHOD, context)
        if method != 0:
            commands.append("-" + LasGrid.METHODS[method])
        if self.parameterAsBool(parameters, LasGrid.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"": None}

    def createInstance(self):
        return LasGrid()

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


class LasGridPro(LastoolsAlgorithm):
    TOOL_NAME = "LasGridPro"
    LASTOOL = "lasgrid"
    LICENSE = "c"
    LASGROUP = 5
    ATTRIBUTE = "ATTRIBUTE"
    METHOD = "METHOD"
    ATTRIBUTES = ["elevation", "intensity", "rgb", "classification"]
    METHODS = ["lowest", "highest", "average", "stddev"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_point_input_merged_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_step_gui()
        self.addParameter(
            QgsProcessingParameterEnum(LasGridPro.ATTRIBUTE, "Attribute", LasGridPro.ATTRIBUTES, False, 0)
        )
        self.addParameter(QgsProcessingParameterEnum(LasGridPro.METHOD, "Method", LasGridPro.METHODS, False, 0))
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasGridPro.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_point_input_merged_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_step_commands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, LasGridPro.ATTRIBUTE, context)
        if attribute != 0:
            commands.append("-" + LasGridPro.ATTRIBUTES[attribute])
        method = self.parameterAsInt(parameters, LasGridPro.METHOD, context)
        if method != 0:
            commands.append("-" + LasGridPro.METHODS[method])
        if self.parameterAsBool(parameters, LasGridPro.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasGridPro()

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
