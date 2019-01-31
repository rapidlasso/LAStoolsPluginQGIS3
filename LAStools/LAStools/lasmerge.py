# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasmerge.py
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
from qgis.core import QgsProcessingParameterFile

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasmerge(LAStoolsAlgorithm):

    FILE2 = "FILE2"
    FILE3 = "FILE3"
    FILE4 = "FILE4"
    FILE5 = "FILE5"
    FILE6 = "FILE6"
    FILE7 = "FILE7"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersFilesAreFlightlinesGUI()
        self.addParametersApplyFileSourceIdGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE2, "2nd file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE3, "3rd file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE4, "4th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE5, "5th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE6, "6th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE7, "7th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasmerge.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasmerge")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        file2 = self.parameterAsString(parameters, lasmerge.FILE2, context)
        if file2 is not None:
            commands.append("-i")
            commands.append(file2)
        file3 = self.parameterAsString(parameters, lasmerge.FILE3, context)
        if file3 is not None:
            commands.append("-i")
            commands.append(file3)
        file4 = self.parameterAsString(parameters, lasmerge.FILE4, context)
        if file4 is not None:
            commands.append("-i")
            commands.append(file4)
        file5 = self.parameterAsString(parameters, lasmerge.FILE5, context)
        if file5 is not None:
            commands.append("-i")
            commands.append(file5)
        file6 = self.parameterAsString(parameters, lasmerge.FILE6, context)
        if file6 is not None:
            commands.append("-i")
            commands.append(file6)
        file7 = self.parameterAsString(parameters, lasmerge.FILE7, context)
        if file7 is not None:
            commands.append("-i")
            commands.append(file7)
        self.addParametersFilesAreFlightlinesCommands(parameters, context, commands)
        self.addParametersApplyFileSourceIdCommands(parameters, context, commands)
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasmerge'

    def displayName(self):
        return 'lasmerge'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return lasmerge()
