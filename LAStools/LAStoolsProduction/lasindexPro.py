# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasindexPro.py
    ---------------------
    Date                 : October 2014, May 2016 and August 2018
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
__date__ = 'October 2014'
__copyright__ = '(C) 2014, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasindexPro(LAStoolsAlgorithm):

    MOBILE_OR_TERRESTRIAL = "MOBILE_OR_TERRESTRIAL"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterBoolean(lasindexPro.APPEND_LAX, "append *.lax file to *.laz file", False))
        self.addParameter(QgsProcessingParameterBoolean(lasindexPro.MOBILE_OR_TERRESTRIAL, "is mobile or terrestrial LiDAR (not airborne)", False))
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasindex.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasindex")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasindexPro.APPEND_LAX, context)):
            commands.append("-append")
        if (self.parameterAsBool(parameters, lasindexPro.MOBILE_OR_TERRESTRIAL, context)):
            commands.append("-tile_size")
            commands.append("10")
            commands.append("-maximum")
            commands.append("-100")
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasindexPro'

    def displayName(self):
        return 'lasindexPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasindexPro()

