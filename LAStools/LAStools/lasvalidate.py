# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasvalidate.py
    ---------------------
    Date                 : September 2013 and August 2018
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
from processing.core.outputs import OutputFile

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasvalidate(LAStoolsAlgorithm):

    ONE_REPORT_PER_FILE = "ONE_REPORT_PER_FILE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasvalidate')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterBoolean(lasvalidate.ONE_REPORT_PER_FILE,
                                           self.tr("save report to '*_LVS.xml'"), False))
        self.addOutput(OutputFile(lasvalidate.OUTPUT, self.tr("Output XML file")))
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasvalidate")]
        self.addParametersPointInputCommands(parameters, context, commands)
        if self.parameterAsInt(parameters, lasvalidate.ONE_REPORT_PER_FILE):
            commands.append("-oxml")
        else:
            commands.append("-o")
            commands.append(self.getOutputValue(lasvalidate.OUTPUT))
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'LAStools'

    def groupId(self):
        return 'LAStools'

    def createInstance(self):
        return laszip()
	