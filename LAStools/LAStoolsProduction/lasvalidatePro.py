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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from processing.core.outputs import OutputFile


class lasvalidatePro(LAStoolsAlgorithm):

    ONE_REPORT_PER_FILE = "ONE_REPORT_PER_FILE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasvalidatePro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParameter(ParameterBoolean(lasvalidatePro.ONE_REPORT_PER_FILE,
                                           self.tr("generate one '*_LVS.xml' report per file"), False))
        self.addOutput(OutputFile(lasvalidatePro.OUTPUT, self.tr("Output XML file")))
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasvalidate")]
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if self.getParameterValue(lasvalidatePro.ONE_REPORT_PER_FILE):
            commands.append("-oxml")
        else:
            commands.append("-o")
            commands.append(self.getOutputValue(lasvalidatePro.OUTPUT))
        self.addParametersAdditionalCommands(parameters, context, commands)

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
	
