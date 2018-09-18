# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasground.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasground(LAStoolsAlgorithm):

    NO_BULGE = "NO_BULGE"
    BY_FLIGHTLINE = "BY_FLIGHTLINE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersHorizontalAndVerticalFeetGUI()
        self.addParameter(QgsProcessingParameterBoolean(lasground.NO_BULGE, "no triangle bulging during TIN refinement", False))
        self.addParameter(QgsProcessingParameterBoolean(lasground.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False))
        self.addParameter(QgsProcessingParameterEnum(lasground.TERRAIN, "terrain type", lasground.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(lasground.GRANULARITY, "preprocessing", lasground.GRANULARITIES, False, 1))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersHorizontalAndVerticalFeetCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasground.NO_BULGE, context)):
            commands.append("-no_bulge")
        if (self.parameterAsBool(parameters, lasground.BY_FLIGHTLINE, context)):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, lasground.TERRAIN, context)
        if (method != 2):
            commands.append("-" + lasground.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, lasground.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + lasground.GRANULARITIES[granularity])
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasground'

    def displayName(self):
        return 'lasground'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasground()
