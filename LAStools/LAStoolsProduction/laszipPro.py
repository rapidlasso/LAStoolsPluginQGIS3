# -*- coding: utf-8 -*-

"""
***************************************************************************
    laszipPro.py
    ---------------------
    Date                 : October 2014 and August 2018, August 2018
    Copyright            : (C) 2014 - 2018 by Martin Isenburg
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

class laszipPro(LAStoolsAlgorithm):

    REPORT_SIZE = "REPORT_SIZE"
    CREATE_LAX = "CREATE_LAX"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterBoolean(laszipPro.REPORT_SIZE, "only report size", False))
        self.addParameter(QgsProcessingParameterBoolean(laszipPro.CREATE_LAX, "create spatial indexing file (*.lax)", False))
        self.addParameter(QgsProcessingParameterBoolean(laszipPro.APPEND_LAX, "append *.lax into *.laz file", False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "laszip.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "laszip")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if self.parameterAsBool(parameters, laszipPro.REPORT_SIZE, context):
            commands.append("-size")
        if self.parameterAsBool(parameters, laszipPro.CREATE_LAX, context):
            commands.append("-lax")
        if self.parameterAsBool(parameters, laszipPro.APPEND_LAX, context):
            commands.append("-append")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszipPro'

    def displayName(self):
        return 'laszipPro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return laszipPro()
	