# -*- coding: utf-8 -*-

"""
***************************************************************************
    laszip.py
    ---------------------
    Date                 : September 2013 and August 2018, August 2018
    Copyright            : (C) 2013 - 2018 by Martin Isenburg
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

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm
	
class laszip(LAStoolsAlgorithm):

    REPORT_SIZE = "REPORT_SIZE"
    CREATE_LAX = "CREATE_LAX"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterBoolean(laszip.REPORT_SIZE, "only report size", False))
        self.addParameter(QgsProcessingParameterBoolean(laszip.CREATE_LAX, "create spatial indexing file (*.lax)", False))
        self.addParameter(QgsProcessingParameterBoolean(laszip.APPEND_LAX, "append *.lax into *.laz file", False))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "laszip.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "laszip")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        if self.parameterAsBool(parameters, laszip.REPORT_SIZE, context):
            commands.append("-size")
        if self.parameterAsBool(parameters, laszip.CREATE_LAX, context):
            commands.append("-lax")
        if self.parameterAsBool(parameters, laszip.APPEND_LAX, context):
            commands.append("-append")
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
		
        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return laszip()
	