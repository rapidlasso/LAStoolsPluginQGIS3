# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoveragePro.py
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

from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum


class lasoveragePro(LAStoolsAlgorithm):

    CHECK_STEP = "CHECK_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify as overlap", "flag as withheld", "remove from output"]

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasoveragePro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersHorizontalFeetGUI()
        self.addParametersFilesAreFlightlinesGUI()
        self.addParameter(ParameterNumber(lasoveragePro.CHECK_STEP,
                                          self.tr("size of grid used for scan angle check"), 0, None, 1.0))
        self.addParameter(ParameterSelection(lasoveragePro.OPERATION,
                                             self.tr("mode of operation"), lasoveragePro.OPERATIONS, 0))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasoverage")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersHorizontalFeetCommands(parameters, context, commands)
        self.addParametersFilesAreFlightlinesCommands(parameters, context, commands)
        step = self.getParameterValue(lasoveragePro.CHECK_STEP)
        if step != 1.0:
            commands.append("-step")
            commands.append(unicode(step))
        operation = self.getParameterValue(lasoveragePro.OPERATION)
        if operation == 1:
            commands.append("-flag_as_withheld")
        elif operation == 2:
            commands.append("-remove_overage")
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
	
