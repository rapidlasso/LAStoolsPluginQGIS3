# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasnoise.py
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

__author__ = 'Martin Isenburg'
__date__ = 'September 2013'
__copyright__ = '(C) 2013, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasnoise(LAStoolsAlgorithm):

    ISOLATED = "ISOLATED"
    STEP_XY = "STEP_XY"
    STEP_Z = "STEP_Z"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify", "remove"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(QgsProcessingParameterNumber(lasnoise.ISOLATED, "isolated if surrounding cells have only", QgsProcessingParameterNumber.Integer, 5, False, 1))
        self.addParameter(QgsProcessingParameterNumber(lasnoise.STEP_XY, "resolution of isolation grid in xy", QgsProcessingParameterNumber.Double, 4.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(lasnoise.STEP_Z, "resolution of isolation grid in z", QgsProcessingParameterNumber.Double, 4.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(lasnoise.OPERATION, "what to do with isolated points", lasnoise.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasnoise.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 7, False, 0, 255))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasnoise")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        isolated = self.parameterAsInt(parameters, lasnoise.ISOLATED, context)
        commands.append("-isolated")
        commands.append(unicode(isolated))
        step_xy = self.parameterAsDouble(parameters, lasnoise.STEP_XY, context)
        commands.append("-step_xy")
        commands.append(unicode(step_xy))
        step_z = self.parameterAsDouble(parameters, lasnoise.STEP_Z, context)
        commands.append("-step_z")
        commands.append(unicode(step_z))
        operation = self.parameterAsInt(parameters, lasnoise.OPERATION, context)
        if (operation != 0):
            commands.append("-remove_noise")
        else:
            commands.append("-classify_as")
            classify_as = self.parameterAsInt(parameters, lasnoise.CLASSIFY_AS, context)
            commands.append(unicode(classify_as))
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasnoise'

    def displayName(self):
        return 'lasnoise'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasnoise()
