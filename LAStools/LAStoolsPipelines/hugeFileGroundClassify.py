# -*- coding: utf-8 -*-

"""
***************************************************************************
    hugeFileGroundClassify.py
    ---------------------
    Date                 : May 2014 and August 2018
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
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum
					   
from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class hugeFileGroundClassify(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    AIRBORNE = "AIRBORNE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterNumber(hugeFileGroundClassify.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(hugeFileGroundClassify.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterBoolean(hugeFileGroundClassify.AIRBORNE, "airborne LiDAR", True))
        self.addParameter(QgsProcessingParameterEnum(hugeFileGroundClassify.TERRAIN, "terrain type", hugeFileGroundClassify.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(hugeFileGroundClassify.GRANULARITY, "preprocessing", hugeFileGroundClassify.GRANULARITIES, False, 1))
        self.add_parameters_temporary_directory_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):

        # first we tile the data with option '-reversible'

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        tile_size = self.parameterAsDouble(parameters, hugeFileGroundClassify.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, hugeFileGroundClassify.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        commands.append("-reversible")
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-o")
        commands.append("hugeFileGroundClassify.laz")

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we ground classify the reversible tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "hugeFileGroundClassify*.laz")
        airborne = self.parameterAsBool(parameters, hugeFileGroundClassify.AIRBORNE, context)
        if (not airborne):
            commands.append("-not_airborne")
        method = self.parameterAsInt(parameters, hugeFileGroundClassify.TERRAIN, context)
        if (method != 2):
            commands.append("-" + hugeFileGroundClassify.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, hugeFileGroundClassify.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + hugeFileGroundClassify.GRANULARITIES[granularity])
        self.add_parameters_temporary_directory_as_output_directory_commands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we reverse the tiling

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_temporary_directory_as_input_files_commands(parameters, context, commands, "hugeFileGroundClassify*_g.laz")
        commands.append("-reverse_tiling")
        self.add_parameters_point_output_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'hugeFileGroundClassify'

    def displayName(self):
        return 'hugeFileGroundClassify'

    def group(self):
        return 'pipeline - file'

    def groupId(self):
        return 'pipeline - file'

    def createInstance(self):
        return hugeFileGroundClassify()
