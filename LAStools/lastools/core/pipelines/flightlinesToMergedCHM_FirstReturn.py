# -*- coding: utf-8 -*-

"""
***************************************************************************
    flightlinesToMergedCHM_FirstReturn.py
    ---------------------
    Date                 : May 2014 and September 2018
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

__author__ = 'Martin Isenburg'
__date__ = 'May 2014'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class flightlinesToMergedCHM_FirstReturn(LastoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterNumber(flightlinesToMergedCHM_FirstReturn.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(flightlinesToMergedCHM_FirstReturn.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(flightlinesToMergedCHM_FirstReturn.TERRAIN, "terrain type", flightlinesToMergedCHM_FirstReturn.TERRAINS, False, 2))      
        self.add_parameters_step_gui()
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):

        # needed for thinning and killing

        step = self.get_parameters_step_value(parameters, context)

        # first we tile the data

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, flightlinesToMergedCHM_FirstReturn.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, flightlinesToMergedCHM_FirstReturn.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("tile.laz")

        LastoolsUtils.run_lastools(commands, feedback)

        # then we ground classify the tiles

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*.laz")
        method = self.parameterAsInt(parameters, flightlinesToMergedCHM_FirstReturn.TERRAIN, context)
        if (method != 2):
            commands.append("-" + flightlinesToMergedCHM_FirstReturn.TERRAINS[method])
        if (method > 3):
            commands.append("-ultra_fine")
        elif (method > 2):
            commands.append("-extra_fine")
        elif (method > 1):
            commands.append("-fine")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we height-normalize the tiles

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_g.laz")
        commands.append("-replace_z")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we rasterize the height-normalized tiles into trivial zero-level DTMs

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_class")        
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(unicode(step))        
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_dtm")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we rasterize the normalized tiles into first-return CHMs (with kill)

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_first")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-kill")
        commands.append(unicode(step * 3))
        commands.append("-use_tile_bb")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_chm_fr")
        commands.append("-obil")
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        # then we combine the zero-level DTMs and the first-return CHMs into a single output CHM

        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasgrid")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "tile_*.bil")
        commands.append("-merged")
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-highest")
        self.add_parameters_raster_output_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'flightlinesToMergedCHM_FirstReturn'

    def displayName(self):
        return 'flightlinesToMergedCHM_FirstReturn'

    def group(self):
        return 'pipeline - strips'

    def groupId(self):
        return 'pipeline - strips'

    def createInstance(self):
        return flightlinesToMergedCHM_FirstReturn()
