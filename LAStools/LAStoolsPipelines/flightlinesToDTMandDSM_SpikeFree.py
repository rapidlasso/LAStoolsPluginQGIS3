# -*- coding: utf-8 -*-

"""
***************************************************************************
    flightlinesToDTMandDSM_SpikeFree.py
    ---------------------
    Date                 : April 2014 and August 2018
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
from qgis.core import QgsProcessingParameterString

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class flightlinesToDTMandDSM_SpikeFree(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    FREEZE_VALUE = "FREEZE_VALUE"
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterNumber(flightlinesToDTMandDSM_SpikeFree.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(flightlinesToDTMandDSM_SpikeFree.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(flightlinesToDTMandDSM_SpikeFree.TERRAIN, "terrain type", flightlinesToDTMandDSM_SpikeFree.TERRAINS, False, 2))
        self.add_parameters_step_gui()
        self.addParameter(QgsProcessingParameterNumber(flightlinesToDTMandDSM_SpikeFree.FREEZE_VALUE, "spike-free freeze value (by default 3 times step)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0))
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_output_directory_gui()
        self.addParameter(QgsProcessingParameterString(flightlinesToDTMandDSM_SpikeFree.BASE_NAME, "tile base name (using 'sydney' creates sydney_274000_4714000...)", "tile"))
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):
    
        # needed for thinning and spike-free

        step = self.get_parameters_step_value(parameters, context)

        # first we tile the data

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, flightlinesToDTMandDSM_SpikeFree.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, flightlinesToDTMandDSM_SpikeFree.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, flightlinesToDTMandDSM_SpikeFree.BASE_NAME, context)
        if base_name == "":
            base_name = "tile"
        commands.append("-o")
        commands.append(base_name)
        commands.append("-olaz")

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we ground classify the tiles
 
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, base_name + "*.laz")
        method = self.parameterAsInt(parameters, flightlinesToDTMandDSM_SpikeFree.TERRAIN, context)
        if (method != 2):
            commands.append("-" + flightlinesToDTMandDSM_SpikeFree.TERRAINS[method])
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

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we rasterize the classified tiles into DTMs

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, base_name + "*_g.laz")
        commands.append("-keep_class")
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(unicode(step/2))
        self.add_parameters_step_commands(parameters, context, commands)
        commands.append("-use_tile_bb")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("2")
        commands.append("-odix")
        commands.append("_dtm")
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we rasterize the classified tiles into spike-free DSMs

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, base_name + "*_g.laz")
        self.add_parameters_step_commands(parameters, context, commands)
        freeze_value = self.parameterAsDouble(parameters, flightlinesToDTMandDSM_SpikeFree.FREEZE_VALUE, context)
        commands.append("-spike_free")
        if (freeze_value == 0.0):
            commands.append(unicode(3*step))
        else:
            commands.append(unicode(freeze_value))
        commands.append("-use_tile_bb")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("2")
        commands.append("-odix")
        commands.append("_dsm")
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'flightlinesToDTMandDSM_SpikeFree'

    def displayName(self):
        return 'flightlinesToDTMandDSM_SpikeFree'

    def group(self):
        return 'pipeline - strips'

    def groupId(self):
        return 'pipeline - strips'

    def createInstance(self):
        return flightlinesToDTMandDSM_SpikeFree()
