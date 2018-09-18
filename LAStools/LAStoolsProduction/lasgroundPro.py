# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgroundPro.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasgroundPro(LAStoolsAlgorithm):

    NO_BULGE = "NO_BULGE"
    BY_FLIGHTLINE = "BY_FLIGHTLINE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersHorizontalAndVerticalFeetGUI()
        self.addParameter(QgsProcessingParameterBoolean(lasgroundPro.NO_BULGE, "no triangle bulging during TIN refinement", False))
        self.addParameter(QgsProcessingParameterBoolean(lasgroundPro.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False))
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro.TERRAIN, "terrain type", lasgroundPro.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro.GRANULARITY, "preprocessing", lasgroundPro.GRANULARITIES, False, 1))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersHorizontalAndVerticalFeetCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasgroundPro.NO_BULGE, context)):
            commands.append("-no_bulge")
        if (self.parameterAsBool(parameters, lasgroundPro.BY_FLIGHTLINE, context)):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, lasgroundPro.TERRAIN, context)
        if (method != 2):
            commands.append("-" + lasgroundPro.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, lasgroundPro.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + lasgroundPro.GRANULARITIES[granularity])
        self.addParametersCoresCommands(parameters, context, commands)
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasgroundPro'

    def displayName(self):
        return 'lasgroundPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasgroundPro()
