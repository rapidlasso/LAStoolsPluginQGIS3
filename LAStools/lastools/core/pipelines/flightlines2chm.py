"""
***************************************************************************
    flightlines2chm.py
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

from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterNumber, QgsProcessingParameterString
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class FlightLinesToCHMFirstReturn(LastoolsAlgorithm):
    TOOL_NAME = "FlightLinesToCHMFirstReturn"
    LASTOOL = "flightlines2chm"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMFirstReturn.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMFirstReturn.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                FlightLinesToCHMFirstReturn.TERRAIN, "terrain type", FlightLinesToCHMFirstReturn.TERRAINS, False, 2
            )
        )
        self.add_parameters_step_gui()
        self.add_parameters_temporary_directory_gui()
        self.addParameter(
            QgsProcessingParameterString(
                FlightLinesToCHMFirstReturn.BASE_NAME,
                "tile base name (using 'sydney' creates sydney_274000_4714000...)",
                "tile",
            )
        )
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui()
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # first we tile the data
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, FlightLinesToCHMFirstReturn.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, FlightLinesToCHMFirstReturn.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, FlightLinesToCHMFirstReturn.BASE_NAME, context)
        if base_name == "":
            base_name = "tile"
        commands.append("-o")
        commands.append(base_name)
        commands.append("-olaz")
        LastoolsUtils.run_lastools(commands, feedback)

        # then we ground classify the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*.laz"
        )
        method = self.parameterAsInt(parameters, FlightLinesToCHMFirstReturn.TERRAIN, context)
        if method != 2:
            commands.append("-" + FlightLinesToCHMFirstReturn.TERRAINS[method])
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

        LastoolsUtils.run_lastools(commands, feedback)

        # then we height-normalize the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_g.laz"
        )
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into CHMs
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_gh.laz"
        )
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-use_tile_bb")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_chm_fr")
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return FlightLinesToCHMFirstReturn()

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


class FlightLinesToCHMHighestReturn(LastoolsAlgorithm):
    TOOL_NAME = "FlightLinesToCHMHighestReturn"
    LASTOOL = "flightlines2chm"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BEAM_WIDTH = "BEAM_WIDTH"
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMHighestReturn.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMHighestReturn.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                FlightLinesToCHMHighestReturn.TERRAIN, "terrain type", FlightLinesToCHMHighestReturn.TERRAINS, False, 2
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMHighestReturn.BEAM_WIDTH,
                "laser beam width (diameter of laser footprint)",
                QgsProcessingParameterNumber.Double,
                0.2,
                False,
                0.0,
            )
        )
        self.add_parameters_step_gui()
        self.add_parameters_temporary_directory_gui()
        self.addParameter(
            QgsProcessingParameterString(
                FlightLinesToCHMHighestReturn.BASE_NAME,
                "tile base name (using 'sydney' creates sydney_274000_4714000...)",
                "tile",
            )
        )
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # first we tile the data
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, FlightLinesToCHMHighestReturn.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, FlightLinesToCHMHighestReturn.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, FlightLinesToCHMHighestReturn.BASE_NAME, context)
        if base_name == "":
            base_name = "tile"
        commands.append("-o")
        commands.append(base_name)
        commands.append("-olaz")

        LastoolsUtils.run_lastools(commands, feedback)

        # then we ground classify the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*.laz"
        )
        method = self.parameterAsInt(parameters, FlightLinesToCHMHighestReturn.TERRAIN, context)
        if method != 2:
            commands.append("-" + FlightLinesToCHMHighestReturn.TERRAINS[method])
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

        LastoolsUtils.run_lastools(commands, feedback)

        # then we height-normalize the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_g.laz"
        )
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we thin and splat the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasthin" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_gh.laz"
        )
        beam_width = self.parameterAsDouble(parameters, FlightLinesToCHMHighestReturn.BEAM_WIDTH, context)
        if beam_width != 0.0:
            commands.append("-subcircle")
            commands.append(str(beam_width / 2))
        step = self.get_parameters_step_value(parameters, context)
        commands.append("-step")
        commands.append(str(step / 2))
        commands.append("-highest")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("t")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into CHMs
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_ght.laz"
        )
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-use_tile_bb")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm_hr")
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return FlightLinesToCHMHighestReturn()

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


class FlightLinesToCHMSpikeFree(LastoolsAlgorithm):
    TOOL_NAME = "FlightLinesToCHMSpikeFree"
    LASTOOL = "flightlines2chm"
    LICENSE = "c"
    LASGROUP = 9
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BEAM_WIDTH = "BEAM_WIDTH"
    FREEZE_VALUE = "FREEZE_VALUE"
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMSpikeFree.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMSpikeFree.BUFFER,
                "buffer around tiles (avoids edge artifacts)",
                QgsProcessingParameterNumber.Double,
                25.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                FlightLinesToCHMSpikeFree.TERRAIN, "terrain type", FlightLinesToCHMSpikeFree.TERRAINS, False, 2
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMSpikeFree.BEAM_WIDTH,
                "laser beam width (diameter of laser footprint)",
                QgsProcessingParameterNumber.Double,
                0.2,
                False,
                0.0,
            )
        )
        self.add_parameters_step_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                FlightLinesToCHMSpikeFree.FREEZE_VALUE,
                "spike-free freeze value (by default 3 times step)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
            )
        )
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_output_directory_gui()
        self.addParameter(
            QgsProcessingParameterString(
                FlightLinesToCHMSpikeFree.BASE_NAME,
                "tile base name (using 'sydney' creates sydney_274000_4714000...)",
                "tile",
            )
        )
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # needed for thinning and spike-free

        step = self.get_parameters_step_value(parameters, context)

        # first we tile the data

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, FlightLinesToCHMSpikeFree.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, FlightLinesToCHMSpikeFree.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, FlightLinesToCHMSpikeFree.BASE_NAME, context)
        if base_name == "":
            base_name = "tile"
        commands.append("-o")
        commands.append(base_name)
        commands.append("-olaz")

        LastoolsUtils.run_lastools(commands, feedback)

        # then we ground classify the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*.laz"
        )
        method = self.parameterAsInt(parameters, FlightLinesToCHMSpikeFree.TERRAIN, context)
        if method != 2:
            commands.append("-" + FlightLinesToCHMSpikeFree.TERRAINS[method])
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

        LastoolsUtils.run_lastools(commands, feedback)

        # then we height-normalize the tiles

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_g.laz"
        )
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we thin and splat the tiles
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasthin" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_gh.laz"
        )
        beam_width = self.parameterAsDouble(parameters, FlightLinesToCHMSpikeFree.BEAM_WIDTH, context)
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

        LastoolsUtils.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into CHMs

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem" + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(
            parameters, context, commands, base_name + "*_ght.laz"
        )
        self.add_parameters_step_commands(parameters, context, commands)
        freeze_value = self.parameterAsDouble(parameters, FlightLinesToCHMSpikeFree.FREEZE_VALUE, context)
        commands.append("-spike_free")
        if freeze_value == 0.0:
            commands.append(str(3 * step))
        else:
            commands.append(str(freeze_value))
        commands.append("-use_tile_bb")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm_sf")
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return FlightLinesToCHMSpikeFree()

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
