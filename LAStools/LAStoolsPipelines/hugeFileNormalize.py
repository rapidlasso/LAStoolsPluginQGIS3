# -*- coding: utf-8 -*-

"""
***************************************************************************
    hugeFileNormalize.py
    ---------------------
    Date                 : May 2014 and August 2018
    Copyright            : (C) 2014 by Martin Isenburg
    Email                : martin near rapidlasso point com
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
__copyright__ = '(C) 2014, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class hugeFileNormalize(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    AIRBORNE = "AIRBORNE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(hugeFileNormalize.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(hugeFileNormalize.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterBoolean(hugeFileNormalize.AIRBORNE, "airborne LiDAR", True))
        self.addParameter(QgsProcessingParameterEnum(hugeFileNormalize.TERRAIN, "terrain type", hugeFileNormalize.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(hugeFileNormalize.GRANULARITY, "preprocessing", hugeFileNormalize.GRANULARITIES, False, 1))
        self.addParametersTemporaryDirectoryGUI()
        self.addParametersPointOutputGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):

        # first we tile the data with option '-reversible'

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        tile_size = self.parameterAsDouble(parameters, hugeFileNormalize.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, hugeFileNormalize.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        commands.append("-reversible")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-o")
        commands.append("hugeFileNormalize.laz")

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we ground classify the reversible tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "hugeFileNormalize*.laz")
        airborne = self.parameterAsBool(parameters, hugeFileNormalize.AIRBORNE, context)
        if (not airborne):
            commands.append("-not_airborne")
        method = self.parameterAsInt(parameters, hugeFileNormalize.TERRAIN, context)
        if (method != 2):
            commands.append("-" + hugeFileNormalize.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, hugeFileNormalize.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + hugeFileNormalize.GRANULARITIES[granularity])
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we height-normalize each points in the reversible tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "hugeFileNormalize*_g.laz")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-replace_z")
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we reverse the tiling

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "hugeFileNormalize*_gh.laz")
        commands.append("-reverse_tiling")
        self.addParametersPointOutputCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'hugeFileNormalize'

    def displayName(self):
        return 'hugeFileNormalize'

    def group(self):
        return 'pipeline - file'

    def groupId(self):
        return 'pipeline - file'

    def createInstance(self):
        return hugeFileNormalize()
