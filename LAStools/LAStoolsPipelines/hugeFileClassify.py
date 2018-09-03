# -*- coding: utf-8 -*-

"""
***************************************************************************
    hugeFileClassify.py
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

class hugeFileClassify(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    AIRBORNE = "AIRBORNE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(hugeFileClassify.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(hugeFileClassify.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterBoolean(hugeFileClassify.AIRBORNE, "airborne LiDAR", True))
        self.addParameter(QgsProcessingParameterEnum(hugeFileClassify.TERRAIN, "terrain type", hugeFileClassify.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(hugeFileClassify.GRANULARITY, "preprocessing", hugeFileClassify.GRANULARITIES, False, 1))
        self.addParametersTemporaryDirectoryGUI()
        self.addParametersPointOutputGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):

        # first we tile the data with option '-reversible'

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        tile_size = self.parameterAsDouble(parameters, hugeFileClassify.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, hugeFileClassify.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        commands.append("-reversible")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-o")
        commands.append("hugeFileClassify.laz")

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we ground classify the reversible tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "hugeFileClassify*.laz")
        airborne = self.parameterAsBool(parameters, hugeFileClassify.AIRBORNE, context)
        if (not airborne):
            commands.append("-not_airborne")
        method = self.parameterAsInt(parameters, hugeFileClassify.TERRAIN, context)
        if (method != 2):
            commands.append("-" + hugeFileClassify.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, hugeFileClassify.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + hugeFileClassify.GRANULARITIES[granularity])
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we compute the height for each points in the reversible tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "hugeFileClassify*_g.laz")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we classify buildings and trees in the reversible tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasclassify")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "hugeFileClassify*_gh.laz")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-odix")
        commands.append("c")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we reverse the tiling

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "hugeFileClassify*_ghc.laz")
        commands.append("-reverse_tiling")
        self.addParametersPointOutputCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'hugeFileClassify'

    def displayName(self):
        return 'hugeFileClassify'

    def group(self):
        return 'pipeline - file'

    def groupId(self):
        return 'pipeline - file'

    def createInstance(self):
        return hugeFileClassify()
