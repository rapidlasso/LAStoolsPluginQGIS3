# -*- coding: utf-8 -*-

"""
***************************************************************************
    flightlinesToCHM_SpikeFree.py
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
from qgis.core import QgsProcessingParameterString

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class flightlinesToCHM_SpikeFree(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    BEAM_WIDTH = "BEAM_WIDTH"
    FREEZE_VALUE = "FREEZE_VALUE"
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterNumber(flightlinesToCHM_SpikeFree.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(flightlinesToCHM_SpikeFree.BUFFER, "buffer around tiles (avoids edge artifacts)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(flightlinesToCHM_SpikeFree.TERRAIN, "terrain type", flightlinesToCHM_SpikeFree.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterNumber(flightlinesToCHM_SpikeFree.BEAM_WIDTH, "laser beam width (diameter of laser footprint)", QgsProcessingParameterNumber.Double, 0.2, False, 0.0))
        self.addParametersStepGUI()
        self.addParameter(QgsProcessingParameterNumber(flightlinesToCHM_SpikeFree.FREEZE_VALUE, "spike-free freeze value (by default 3 times step)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0))
        self.addParametersTemporaryDirectoryGUI()
        self.addParametersOutputDirectoryGUI()
        self.addParameter(QgsProcessingParameterString(flightlinesToCHM_SpikeFree.BASE_NAME, "tile base name (using 'sydney' creates sydney_274000_4714000...)", "tile"))
        self.addParametersRasterOutputFormatGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):

        # needed for thinning and spike-free

        step = self.getParametersStepValue(parameters, context)

        # first we tile the data

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        commands.append("-files_are_flightlines")
        tile_size = self.parameterAsDouble(parameters, flightlinesToCHM_SpikeFree.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, flightlinesToCHM_SpikeFree.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        self.addParametersTemporaryDirectoryAsOutputDirectoryCommands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, flightlinesToCHM_SpikeFree.BASE_NAME, context)
        if (base_name == ""):
            base_name = "tile"
        commands.append("-o")
        commands.append(base_name)
        commands.append("-olaz")

        LAStoolsUtils.runLAStools(commands, feedback)

        # then we ground classify the tiles

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, base_name + "*.laz")
        method = self.parameterAsInt(parameters, flightlinesToCHM_SpikeFree.TERRAIN, context)
        if (method != 2):
            commands.append("-" + flightlinesToCHM_SpikeFree.TERRAINS[method])
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
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, base_name + "*_g.laz")
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
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, base_name + "*_gh.laz")
        beam_width = self.parameterAsDouble(parameters, flightlinesToCHM_SpikeFree.BEAM_WIDTH, context)
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

        # then we rasterize the normalized tiles into CHMs

        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersTemporaryDirectoryAsInputFilesCommands(parameters, context, commands, base_name + "*_ght.laz")
        self.addParametersStepCommands(parameters, context, commands)
        freeze_value = self.parameterAsDouble(parameters, flightlinesToCHM_SpikeFree.FREEZE_VALUE, context)
        commands.append("-spike_free")
        if (freeze_value == 0.0):
            commands.append(unicode(3*step))
        else:
            commands.append(unicode(freeze_value))
        commands.append("-use_tile_bb")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        commands.append("-ocut")
        commands.append("4")
        commands.append("-odix")
        commands.append("_chm_sf")
        self.addParametersRasterOutputFormatCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)
        
        return {"": None}

    def name(self):
        return 'flightlinesToCHM_SpikeFree'

    def displayName(self):
        return 'flightlinesToCHM_SpikeFree'

    def group(self):
        return 'pipeline - strips'

    def groupId(self):
        return 'pipeline - strips'

    def createInstance(self):
        return flightlinesToCHM_SpikeFree()
