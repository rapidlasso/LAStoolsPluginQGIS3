# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasnoisePro.py
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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum


class lasnoisePro(LAStoolsAlgorithm):

    ISOLATED = "ISOLATED"
    STEP_XY = "STEP_XY"
    STEP_Z = "STEP_Z"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify", "remove"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasnoisePro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(ParameterNumber(lasnoisePro.ISOLATED,
                                          self.tr("isolated if surrounding cells have only"), 0, None, 5))
        self.addParameter(ParameterNumber(lasnoisePro.STEP_XY,
                                          self.tr("resolution of isolation grid in xy"), 0, None, 4.0))
        self.addParameter(ParameterNumber(lasnoisePro.STEP_Z,
                                          self.tr("resolution of isolation grid in z"), 0, None, 4.0))
        self.addParameter(ParameterSelection(lasnoisePro.OPERATION,
                                             self.tr("what to do with isolated points"), lasnoisePro.OPERATIONS, 0))
        self.addParameter(ParameterNumber(lasnoisePro.CLASSIFY_AS,
                                          self.tr("classify as"), 0, None, 7))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasnoise")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        isolated = self.getParameterValue(lasnoisePro.ISOLATED)
        commands.append("-isolated")
        commands.append(unicode(isolated))
        step_xy = self.getParameterValue(lasnoisePro.STEP_XY)
        commands.append("-step_xy")
        commands.append(unicode(step_xy))
        step_z = self.getParameterValue(lasnoisePro.STEP_Z)
        commands.append("-step_z")
        commands.append(unicode(step_z))
        operation = self.getParameterValue(lasnoisePro.OPERATION)
        if operation != 0:
            commands.append("-remove_noise")
        else:
            commands.append("-classify_as")
            classify_as = self.getParameterValue(lasnoisePro.CLASSIFY_AS)
            commands.append(unicode(classify_as))
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
	
