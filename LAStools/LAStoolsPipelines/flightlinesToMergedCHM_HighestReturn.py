# -*- coding: utf-8 -*-

"""
***************************************************************************
    flightlinesToMergedCHM_HighestReturn.py
    ---------------------
    Date                 : May 2014 and September 2018
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

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class flightlinesToMergedCHM_HighestReturn(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BEAM_WIDTH = "BEAM_WIDTH"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterNumber(flightlinesToMergedCHM_HighestReturn.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(flightlinesToMergedCHM_HighestReturn.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(flightlinesToMergedCHM_HighestReturn.TERRAIN, "terrain type", flightlinesToMergedCHM_HighestReturn.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterNumber(flightlinesToMergedCHM_HighestReturn.BEAM_WIDTH, "laser beam width (diameter of laser footprint)", QgsProcessingParameterNumber.Double, 0.2, False, 0.0))       
        self.addParametersStepGUI()
        self.addParametersTemporaryDirectoryGUI()
        self.addParametersRasterOutputGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):

        # needed for thinning and killing

        step = self.getParametersStepValue(parameters, context)

        # first we tile the data

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, flightlinesToMergedCHM_HighestReturn.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, flightlinesToMergedCHM_HighestReturn.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-o")
        commands.append("tile.laz")

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we ground classify the tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "tile*.laz")
        method = self.parameterAsInt(parameters, flightlinesToMergedCHM_HighestReturn.TERRAIN, context)
        if (method != 2):
            commands.append("-" + flightlinesToMergedCHM_HighestReturn.TERRAINS[method])
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

        # then we height-normalize the tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "tile*_g.laz")
        commands.append("-replace_z")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-odix")
        commands.append("h")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we thin and splat the tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasthin")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "tile*_gh.laz")
        beam_width = self.parameterAsDouble(parameters, flightlinesToMergedCHM_HighestReturn.BEAM_WIDTH, context)
        if (beam_width != 0.0):
            commands.append("-subcircle")
            commands.append(unicode(beam_width / 2))
        commands.append("-step")
        commands.append(unicode(step / 2))
        commands.append("-highest")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-odix")
        commands.append("t")
        commands.append("-olaz")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we rasterize the height-normalized tiles into trivial zero-level DTMs

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "tile*_gh.laz")
        commands.append("-keep_class")        
        commands.append("2")
        commands.append("-thin_with_grid")
        commands.append(unicode(step))        
        commands.append("-use_tile_bb")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("3")
        commands.append("-odix")
        commands.append("_dtm")
        commands.append("-obil")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we rasterize the normalized tiles into highest-return CHMs (with kill)

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "tile*_ght.laz")
        self.addParametersStepCommands(parameters, context, commands)
        commands.append("-kill")
        commands.append(unicode(step * 3))
        commands.append("-use_tile_bb")
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm_hr")
        commands.append("-obil")
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we combine the zero-level DTMs and the highest-return CHMs into a single output CHM

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasgrid")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, "tile_*.bil")
        commands.append("-merged")
        self.addParametersStepCommands(parameters, context, commands)
        commands.append("-highest")
        self.addParametersRasterOutputCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'flightlinesToMergedCHM_HighestReturn'

    def displayName(self):
        return 'flightlinesToMergedCHM_HighestReturn'

    def group(self):
        return 'pipeline - strips'

    def groupId(self):
        return 'pipeline - strips'

    def createInstance(self):
        return flightlinesToMergedCHM_HighestReturn()
