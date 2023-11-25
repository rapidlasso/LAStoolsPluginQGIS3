# -*- coding: utf-8 -*-

"""
***************************************************************************
    lastile.py
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
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterString
from qgis.core import QgsProcessingParameterNumber

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasTile(LastoolsAlgorithm):
    TOOL_INFO = ('lastile', 'LasTile')
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    REVERSIBLE = "REVERSIBLE"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasTile.TILE_SIZE, "tile size (side length of square tile)",
            QgsProcessingParameterNumber.Double, 1000.0, False, 4.0, 10000.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasTile.BUFFER, "buffer around each tile", QgsProcessingParameterNumber.Double, 30.0, False, 0.0, 100.0
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasTile.FLAG_AS_WITHHELD, "flag buffer points as 'withheld' for easier removal later", True
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasTile.REVERSIBLE, "make tiling reversible (advanced, usually not needed)", False
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        tile_size = self.parameterAsInt(parameters, LasTile.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, LasTile.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        if self.parameterAsBool(parameters, LasTile.FLAG_AS_WITHHELD, context):
            commands.append("-flag_as_withheld")
        if self.parameterAsBool(parameters, LasTile.REVERSIBLE, context):
            commands.append("-reversible")
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasTile()

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


class LasTilePro(LastoolsAlgorithm):
    TOOL_INFO = ('lastile', 'LasTilePro')
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"
    EXTRA_PASS = "EXTRA_PASS"
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_apply_file_source_id_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasTilePro.TILE_SIZE, "tile size (side length of square tile)",
            QgsProcessingParameterNumber.Double, 1000.0, False, 4.0, 10000.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasTilePro.BUFFER, "buffer around each tile", QgsProcessingParameterNumber.Double, 30.0, False, 0.0, 100.0
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasTilePro.FLAG_AS_WITHHELD, "flag buffer points as 'withheld' for easier removal later", True
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasTilePro.EXTRA_PASS, "more than 2000 output tiles", False
        ))
        self.add_parameters_output_directory_gui()
        self.addParameter(QgsProcessingParameterString(
            LasTilePro.BASE_NAME, "tile base name (using sydney.laz creates sydney_274000_4714000.laz)", ""
        ))
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_apply_file_source_id_commands(parameters, context, commands)
        tile_size = self.parameterAsInt(parameters, LasTilePro.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, LasTilePro.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        if self.parameterAsBool(parameters, LasTilePro.FLAG_AS_WITHHELD, context):
            commands.append("-flag_as_withheld")
        if self.parameterAsBool(parameters, LasTilePro.EXTRA_PASS, context):
            commands.append("-extra_pass")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, LasTilePro.BASE_NAME, context)
        if base_name != "":
            commands.append("-o")
            commands.append('"' + base_name + '"')
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasTilePro()

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
