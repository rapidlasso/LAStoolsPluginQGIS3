# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgroundPro_new.py
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2016 by Martin Isenburg
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
__date__ = 'May 2016'
__copyright__ = '(C) 2016 by Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasgroundPro_new(LAStoolsAlgorithm):
    TERRAIN = "TERRAIN"
    TERRAINS = ["wilderness", "nature", "town", "city", "metro", "custom"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine", "hyper_fine"]
    STEP = "STEP"
    BULGE = "BULGE"
    SPIKE = "SPIKE"
    DOWN_SPIKE = "DOWN_SPIKE"
    OFFSET = "OFFSET"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputFolderGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersHorizontalAndVerticalFeetGUI()
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro_new.TERRAIN, "terrain type", lasgroundPro_new.TERRAINS, False, 3))
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro_new.GRANULARITY, "preprocessing", lasgroundPro_new.GRANULARITIES, False, 2))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.STEP, "step (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0, 500.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.BULGE, "bulge (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 2.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.SPIKE, "spike (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.DOWN_SPIKE, "down spike (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.OFFSET, "offset (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 0.05, False, 0.0, 1.0))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground_new")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersHorizontalAndVerticalFeetCommands(parameters, context, commands)
        method = self.parameterAsInt(parameters, lasgroundPro_new.TERRAIN, context)
        if (method == 5):
            commands.append("-step")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.STEP, context)))
            commands.append("-bulge")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.BULGE, context)))
            commands.append("-spike")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.SPIKE, context)))
            commands.append("-spike_down")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.DOWN_SPIKE, context)))
            commands.append("-offset")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.OFFSET, context)))
        else:
            commands.append("-" + lasgroundPro_new.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, lasgroundPro_new.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + lasgroundPro_new.GRANULARITIES[granularity])
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasgroundPro_new'

    def displayName(self):
        return 'lasgroundPro_new'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasgroundPro_new()
