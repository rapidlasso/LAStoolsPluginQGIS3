# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasvalidatePro.py
    ---------------------
    Date                 : October 2014 and August 2018
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

class lasvalidatePro(LAStoolsAlgorithm):

    ONE_REPORT_PER_FILE = "ONE_REPORT_PER_FILE"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterBoolean(lasvalidatePro.ONE_REPORT_PER_FILE, "save report to '*_LVS.xml'", False))
        self.addParametersGenericOutputGUI("Output XML file", "xml", True)
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasvalidate")]
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasvalidatePro.ONE_REPORT_PER_FILE, context)):
            commands.append("-oxml")
        self.addParametersGenericOutputCommands(parameters, context, commands, "-o")
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasvalidatePro'

    def displayName(self):
        return 'lasvalidatePro'

    def group(self):
        return 'folder - checking quality'

    def groupId(self):
        return 'folder - checking quality'

    def createInstance(self):
        return lasvalidatePro()
