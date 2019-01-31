# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasdiff.py
    ---------------------
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
__copyright__ = '(C) 2016, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasdiff(LAStoolsAlgorithm):

    CREATE_DIFFERENCE_FILE = "CREATE_DIFFERENCE_FILE"
    SHUTUP = "SHUTUP"
    SHUTUP_AFTER = ["5", "10", "50", "100", "1000", "10000", "50000"]

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersGenericInputGUI("other input LAS/LAZ file", "laz", False)
        self.addParameter(QgsProcessingParameterEnum(lasdiff.SHUTUP, "stop reporting difference after this many points", lasdiff.SHUTUP_AFTER, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasdiff.CREATE_DIFFERENCE_FILE, "create elevation difference file (if points are in the same order)", False))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasdiff.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasdiff")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersGenericInputCommands(parameters, context, commands, "-i")
        shutup = self.parameterAsInt(parameters, lasdiff.SHUTUP, context)
        if (shutup != 0):
            commands.append("-shutup")
            commands.append(lasdiff.SHUTUP_AFTER[shutup])
        if (self.parameterAsBool(parameters, lasdiff.CREATE_DIFFERENCE_FILE, context)):
            self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasdiff'

    def displayName(self):
        return 'lasdiff'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lasdiff()
