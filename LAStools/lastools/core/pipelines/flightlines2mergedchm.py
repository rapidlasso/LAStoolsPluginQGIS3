# -*- coding: utf-8 -*-
"""
***************************************************************************
    flightlines2mergedchm.py
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

from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class FlightLinesToMergedCHMFirstReturn(LastoolsAlgorithm):
    TOOL_NAME = "FlightLinesToMergedCHMFirstReturn"
    LASTOOL = "flightlines2mergedchm"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMFirstReturn.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMFirstReturn.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                FlightLinesToMergedCHMFirstReturn.TERRAIN,
                "terrain type",
                FlightLinesToMergedCHMFirstReturn.TERRAINS,
                False,
                2,
            )
        )
        self.add_parameters_step_gui()
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # needed for thinning and killing
        step = self.get_parameters_step_value(parameters, context)

        # first we tile the data
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, FlightLinesToMergedCHMFirstReturn.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, FlightLinesToMergedCHMFirstReturn.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("tile.laz")

        self.run_lastools(commands, feedback)

        # then we ground classify the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*.laz")
        method = self.parameterAsInt(parameters, FlightLinesToMergedCHMFirstReturn.TERRAIN, context)
        if method != 2:
            commands.append("-" + FlightLinesToMergedCHMFirstReturn.TERRAINS[method])
        if method > 3:
            commands.append("-ultra_fine")
        elif method > 2:
            commands.append("-extra_fine")
        elif method > 1:
            commands.append("-fine")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we height-normalize the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_g.laz")
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the height-normalized tiles into trivial zero-level DTMs
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_class")
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(str(step))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_dtm")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into first-return CHMs (with kill)
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_first")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_chm_fr")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we combine the zero-level DTMs and the first-return CHMs into a single output CHM
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasgrid")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile_*.bil")
        commands.append("-merged")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-highest")
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return FlightLinesToMergedCHMFirstReturn()

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


class FlightLinesToMergedCHMHighestReturn(LastoolsAlgorithm):
    TOOL_NAME = "FlightLinesToMergedCHMHighestReturn"
    LASTOOL = "flightlines2mergedchm"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BEAM_WIDTH = "BEAM_WIDTH"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMHighestReturn.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMHighestReturn.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                FlightLinesToMergedCHMHighestReturn.TERRAIN,
                "terrain type",
                FlightLinesToMergedCHMHighestReturn.TERRAINS,
                False,
                2,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMHighestReturn.BEAM_WIDTH,
                "laser beam width (diameter of laser footprint)",
                QgsProcessingParameterNumber.Double,
                0.2,
                False,
                0.0,
            )
        )
        self.add_parameters_step_gui()
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # needed for thinning and killing
        step = self.get_parameters_step_value(parameters, context)

        # first we tile the data
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, FlightLinesToMergedCHMHighestReturn.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, FlightLinesToMergedCHMHighestReturn.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("tile.laz")

        self.run_lastools(commands, feedback)

        # then we ground classify the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*.laz")
        method = self.parameterAsInt(parameters, FlightLinesToMergedCHMHighestReturn.TERRAIN, context)
        if method != 2:
            commands.append("-" + FlightLinesToMergedCHMHighestReturn.TERRAINS[method])
        if method > 3:
            commands.append("-ultra_fine")
        elif method > 2:
            commands.append("-extra_fine")
        elif method > 1:
            commands.append("-fine")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we height-normalize the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_g.laz")
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we thin and splat the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasthin")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        beam_width = self.parameterAsDouble(parameters, FlightLinesToMergedCHMHighestReturn.BEAM_WIDTH, context)
        if beam_width != 0.0:
            commands.append("-subcircle")
            commands.append(str(beam_width / 2))
        commands.append("-step")
        commands.append(str(step / 2))
        commands.append("-highest")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("t")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the height-normalized tiles into trivial zero-level DTMs
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_class")
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(str(step))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_dtm")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into highest-return CHMs (with kill)
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm_hr")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we combine the zero-level DTMs and the highest-return CHMs into a single output CHM
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasgrid")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile_*.bil")
        commands.append("-merged")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-highest")
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return FlightLinesToMergedCHMHighestReturn()

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


class FlightLinesToMergedCHMPitFree(LastoolsAlgorithm):
    TOOL_NAME = "FlightLinesToMergedCHMPitFree"
    LASTOOL = "flightlines2mergedchm"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BEAM_WIDTH = "BEAM_WIDTH"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMPitFree.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMPitFree.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                FlightLinesToMergedCHMPitFree.TERRAIN, "terrain type", FlightLinesToMergedCHMPitFree.TERRAINS, False, 2
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMPitFree.BEAM_WIDTH,
                "laser beam width (diameter of laser footprint)",
                QgsProcessingParameterNumber.Double,
                0.2,
                False,
                0.0,
            )
        )
        self.add_parameters_step_gui()
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # needed for thinning and killing
        step = self.get_parameters_step_value(parameters, context)

        # first we tile the data
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, FlightLinesToMergedCHMPitFree.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, FlightLinesToMergedCHMPitFree.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("tile.laz")

        self.run_lastools(commands, feedback)

        # then we ground classify the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*.laz")
        method = self.parameterAsInt(parameters, FlightLinesToMergedCHMPitFree.TERRAIN, context)
        if method != 2:
            commands.append("-" + FlightLinesToMergedCHMPitFree.TERRAINS[method])
        if method > 3:
            commands.append("-ultra_fine")
        elif method > 2:
            commands.append("-extra_fine")
        elif method > 1:
            commands.append("-fine")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we height-normalize the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_g.laz")
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we thin and splat the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasthin")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        beam_width = self.parameterAsDouble(parameters, FlightLinesToMergedCHMPitFree.BEAM_WIDTH, context)
        if beam_width != 0.0:
            commands.append("-subcircle")
            commands.append(str(beam_width / 2))
        commands.append("-step")
        commands.append(str(step / 2))
        commands.append("-highest")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("t")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the height-normalized tiles into trivial zero-level DTMs
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_class")
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(str(step))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_dtm")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into the partial CHMs at level 00
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm00")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into the partial CHMs at level 02
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        commands.append("-drop_z_below")
        commands.append("2.0")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm02")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into the partial CHMs at level 05
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        commands.append("-drop_z_below")
        commands.append("5.0")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm05")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into the partial CHMs at level 10

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        commands.append("-drop_z_below")
        commands.append("10.0")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm10")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into the partial CHMs at level 15

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        commands.append("-drop_z_below")
        commands.append("15.0")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm15")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into the partial CHMs at level 20
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        commands.append("-drop_z_below")
        commands.append("20.0")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm20")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into the partial CHMs at level 25
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        commands.append("-drop_z_below")
        commands.append("25.0")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm25")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we combine the partial CHMs into a single output CHM
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasgrid")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile_*.bil")
        commands.append("-merged")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-highest")
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return FlightLinesToMergedCHMPitFree()

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


class FlightLinesToMergedCHMSpikeFree(LastoolsAlgorithm):
    TOOL_NAME = "FlightLinesToMergedCHMSpikeFree"
    LASTOOL = "flightlines2mergedchm"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BEAM_WIDTH = "BEAM_WIDTH"
    FREEZE_VALUE = "FREEZE_VALUE"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMSpikeFree.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMSpikeFree.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                FlightLinesToMergedCHMSpikeFree.TERRAIN,
                "terrain type",
                FlightLinesToMergedCHMSpikeFree.TERRAINS,
                False,
                2,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMSpikeFree.BEAM_WIDTH,
                "laser beam width (diameter of laser footprint)",
                QgsProcessingParameterNumber.Double,
                0.2,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToMergedCHMSpikeFree.FREEZE_VALUE,
                "spike-free freeze value (by default 3 times step)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
            )
        )

        self.add_parameters_step_gui()
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # needed for thinning and killing
        step = self.get_parameters_step_value(parameters, context)

        # first we tile the data
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, FlightLinesToMergedCHMSpikeFree.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, FlightLinesToMergedCHMSpikeFree.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("tile.laz")

        self.run_lastools(commands, feedback)

        # then we ground classify the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*.laz")
        method = self.parameterAsInt(parameters, FlightLinesToMergedCHMSpikeFree.TERRAIN, context)
        if method != 2:
            commands.append("-" + FlightLinesToMergedCHMSpikeFree.TERRAINS[method])
        if method > 3:
            commands.append("-ultra_fine")
        elif method > 2:
            commands.append("-extra_fine")
        elif method > 1:
            commands.append("-fine")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we height-normalize the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_g.laz")
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we thin and splat the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasthin")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        beam_width = self.parameterAsDouble(parameters, FlightLinesToMergedCHMSpikeFree.BEAM_WIDTH, context)
        if beam_width != 0.0:
            commands.append("-subcircle")
            commands.append(str(beam_width / 2))
        commands.append("-step")
        commands.append(str(step / 2))
        commands.append("-highest")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("t")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the height-normalized tiles into trivial zero-level DTMs
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_class")
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(str(step))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_dtm")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into spike-free CHMs (with kill)
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_ght.laz")
        self.add_parameters_step_commands(parameters, context, commands)
        freeze_value = self.parameterAsDouble(parameters, FlightLinesToMergedCHMSpikeFree.FREEZE_VALUE, context)
        commands.append("-spike_free")
        if freeze_value == 0.0:
            commands.append(str(3 * step))
        else:
            commands.append(str(freeze_value))
        commands.append("-kill")
        commands.append(str(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm_sf")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        # then we combine the zero-level DTMs and the spike-free CHMs into a single output CHM
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasgrid")]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile_*.bil")
        commands.append("-merged")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-highest")
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return FlightLinesToMergedCHMSpikeFree()

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
