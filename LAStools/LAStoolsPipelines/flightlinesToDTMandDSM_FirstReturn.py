# -*- coding: utf-8 -*-

"""
***************************************************************************
    flightlinesToDTMandDSM_FirstReturn.py
    ---------------------
    Date                 : April 2014 and August 2018
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
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterString

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class flightlinesToDTMandDSM_FirstReturn(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterNumber(flightlinesToDTMandDSM_FirstReturn.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(flightlinesToDTMandDSM_FirstReturn.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(flightlinesToDTMandDSM_FirstReturn.TERRAIN, "terrain type", flightlinesToDTMandDSM_FirstReturn.TERRAINS, False, 2))
        self.addParametersStepGUI()
        self.addParametersTemporaryDirectoryGUI()
        self.addParametersOutputDirectoryGUI()
        self.addParameter(QgsProcessingParameterString(flightlinesToDTMandDSM_FirstReturn.BASE_NAME, "tile base name (using 'sydney' creates sydney_274000_4714000...)", "tile"))
        self.addParametersRasterOutputFormatGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
    
        # needed for thinning

        step = self.getParametersStepValue(parameters, context)

        # first we tile the data

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, flightlinesToDTMandDSM_FirstReturn.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, flightlinesToDTMandDSM_FirstReturn.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, flightlinesToDTMandDSM_FirstReturn.BASE_NAME, context)
        if base_name == "":
            base_name = "tile"
        commands.append("-o")
        commands.append(base_name)
        commands.append("-olaz")

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we ground classify the tiles
 
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, base_name + "*.laz")
        method = self.parameterAsInt(parameters, flightlinesToDTMandDSM_FirstReturn.TERRAIN, context)
        if (method != 2):
            commands.append("-" + flightlinesToDTMandDSM_FirstReturn.TERRAINS[method])
        if (method > 3):
            commands.append("-ultra_fine")
        elif (method > 2):
            commands.append("-extra_fine")
        elif (method > 1):
            commands.append("-fine")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-odix")
        commands.append("_g")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we rasterize the classified tiles into DTMs

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, base_name + "*_g.laz")
        commands.append("-keep_class")
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(unicode(step/2))
        self.addParametersStepCommands(parameters, context, commands)
        commands.append("-use_tile_bb")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("2")
        commands.append("-odix")
        commands.append("_dtm")
        self.addParametersRasterOutputFormatCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we rasterize the classified tiles into first return DSMs

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, base_name + "*_g.laz")
        commands.append("-first_only")
        commands.append("-thin_with_grid")
        commands.append(unicode(step/2))
        self.addParametersStepCommands(parameters, context, commands)
        commands.append("-use_tile_bb")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("2")
        commands.append("-odix")
        commands.append("_dsm")
        self.addParametersRasterOutputFormatCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'flightlinesToDTMandDSM_FirstReturn'

    def displayName(self):
        return 'flightlinesToDTMandDSM_FirstReturn'

    def group(self):
        return 'pipeline - strips'

    def groupId(self):
        return 'pipeline - strips'

    def createInstance(self):
        return flightlinesToDTMandDSM_FirstReturn()
