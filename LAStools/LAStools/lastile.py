# -*- coding: utf-8 -*-

"""
***************************************************************************
    lastile.py
    ---------------------
    Date                 : September 2013, May 2016 and August 2018
    Copyright            : (C) 2013 by Martin Isenburg
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
__date__ = 'September 2013'
__copyright__ = '(C) 2013, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lastile(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    REVERSIBLE = "REVERSIBLE"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(lastile.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 4.0, 10000.0))
        self.addParameter(QgsProcessingParameterNumber(lastile.BUFFER, "buffer around each tile", QgsProcessingParameterNumber.Double, 30.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lastile.FLAG_AS_WITHHELD, "flag buffer points as 'withheld' for easier removal later", True))
        self.addParameter(QgsProcessingParameterBoolean(lastile.REVERSIBLE, "make tiling reversible (advanced, usually not needed)", False))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        tile_size = self.parameterAsInt(parameters, lastile.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, lastile.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        if (self.parameterAsBool(parameters, lastile.FLAG_AS_WITHHELD, context)):
            commands.append("-flag_as_withheld")
        if (self.parameterAsBool(parameters, lastile.REVERSIBLE, context)):
            commands.append("-reversible")
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lastile'

    def displayName(self):
        return 'lastile'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return lastile()
