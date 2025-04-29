# -*- coding: utf-8 -*-
"""
***************************************************************************
    hugefile.py
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

from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class HugeFileClassify(LastoolsAlgorithm):
    TOOL_NAME = "HugeFileClassify"
    LASTOOL = "hugefile"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    AIRBORNE = "AIRBORNE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                HugeFileClassify.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                HugeFileClassify.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(HugeFileClassify.AIRBORNE, "airborne LiDAR", True))
        self.addParameter(
            QgsProcessingParameterEnum(HugeFileClassify.TERRAIN, "terrain type", HugeFileClassify.TERRAINS, False, 2)
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                HugeFileClassify.GRANULARITY, "preprocessing", HugeFileClassify.GRANULARITIES, False, 1
            )
        )
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # first we tile the data with option '-reversible'
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        tile_size = self.parameterAsDouble(parameters, HugeFileClassify.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, HugeFileClassify.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        commands.append("-reversible")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("hugeFileClassify.laz")

        self.run_lastools(commands, feedback)

        # then we ground classify the reversible tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileClassify*.laz"
        )
        airborne = self.parameterAsBool(parameters, HugeFileClassify.AIRBORNE, context)
        if not airborne:
            commands.append("-not_airborne")
        method = self.parameterAsInt(parameters, HugeFileClassify.TERRAIN, context)
        if method != 2:
            commands.append("-" + HugeFileClassify.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, HugeFileClassify.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + HugeFileClassify.GRANULARITIES[granularity])
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we compute the height for each points in the reversible tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileClassify*_g.laz"
        )
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we classify buildings and trees in the reversible tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasclassify")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileClassify*_gh.laz"
        )
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("c")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we reverse the tiling
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileClassify*_ghc.laz"
        )
        commands.append("-reverse_tiling")
        self.add_parameters_point_output_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return HugeFileClassify()

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


class HugeFileGroundClassify(LastoolsAlgorithm):
    TOOL_NAME = "HugeFileGroundClassify"
    LASTOOL = "hugefile"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    AIRBORNE = "AIRBORNE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                HugeFileGroundClassify.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                HugeFileGroundClassify.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(HugeFileGroundClassify.AIRBORNE, "airborne LiDAR", True))
        self.addParameter(
            QgsProcessingParameterEnum(
                HugeFileGroundClassify.TERRAIN, "terrain type", HugeFileGroundClassify.TERRAINS, False, 2
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                HugeFileGroundClassify.GRANULARITY, "preprocessing", HugeFileGroundClassify.GRANULARITIES, False, 1
            )
        )
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # first we tile the data with option '-reversible'
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        tile_size = self.parameterAsDouble(parameters, HugeFileGroundClassify.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, HugeFileGroundClassify.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        commands.append("-reversible")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("hugeFileGroundClassify.laz")

        self.run_lastools(commands, feedback)

        # then we ground classify the reversible tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileGroundClassify*.laz"
        )
        airborne = self.parameterAsBool(parameters, HugeFileGroundClassify.AIRBORNE, context)
        if not airborne:
            commands.append("-not_airborne")
        method = self.parameterAsInt(parameters, HugeFileGroundClassify.TERRAIN, context)
        if method != 2:
            commands.append("-" + HugeFileGroundClassify.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, HugeFileGroundClassify.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + HugeFileGroundClassify.GRANULARITIES[granularity])
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we reverse the tiling
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileGroundClassify*_g.laz"
        )
        commands.append("-reverse_tiling")
        self.add_parameters_point_output_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return HugeFileGroundClassify()

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


class HugeFileNormalize(LastoolsAlgorithm):
    TOOL_NAME = "HugeFileNormalize"
    LASTOOL = "hugefile"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    AIRBORNE = "AIRBORNE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                HugeFileNormalize.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                HugeFileNormalize.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(HugeFileNormalize.AIRBORNE, "airborne LiDAR", True))
        self.addParameter(
            QgsProcessingParameterEnum(HugeFileNormalize.TERRAIN, "terrain type", HugeFileNormalize.TERRAINS, False, 2)
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                HugeFileNormalize.GRANULARITY, "preprocessing", HugeFileNormalize.GRANULARITIES, False, 1
            )
        )
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # first we tile the data with option '-reversible'
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        tile_size = self.parameterAsDouble(parameters, HugeFileNormalize.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, HugeFileNormalize.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        commands.append("-reversible")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("hugeFileNormalize.laz")

        self.run_lastools(commands, feedback)

        # then we ground classify the reversible tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileNormalize*.laz"
        )
        airborne = self.parameterAsBool(parameters, HugeFileNormalize.AIRBORNE, context)
        if not airborne:
            commands.append("-not_airborne")
        method = self.parameterAsInt(parameters, HugeFileNormalize.TERRAIN, context)
        if method != 2:
            commands.append("-" + HugeFileNormalize.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, HugeFileNormalize.GRANULARITY, context)
        if granularity != 1:
            commands.append("-" + HugeFileNormalize.GRANULARITIES[granularity])
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we height-normalize each points in the reversible tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileNormalize*_g.laz"
        )
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-replace_z")
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we reverse the tiling
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, "hugeFileNormalize*_gh.laz"
        )
        commands.append("-reverse_tiling")
        self.add_parameters_point_output_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return HugeFileNormalize()

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
