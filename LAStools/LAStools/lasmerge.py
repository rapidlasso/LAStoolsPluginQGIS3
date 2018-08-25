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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from processing.core.parameters import ParameterFile


class lasmerge(LAStoolsAlgorithm):

    FILE2 = "FILE2"
    FILE3 = "FILE3"
    FILE4 = "FILE4"
    FILE5 = "FILE5"
    FILE6 = "FILE6"
    FILE7 = "FILE7"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasmerge')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersFilesAreFlightlinesGUI()
        self.addParametersApplyFileSourceIdGUI()
        self.addParametersPointInputGUI()
        self.addParameter(ParameterFile(lasmerge.FILE2, self.tr("2nd file")))
        self.addParameter(ParameterFile(lasmerge.FILE3, self.tr("3rd file")))
        self.addParameter(ParameterFile(lasmerge.FILE4, self.tr("4th file")))
        self.addParameter(ParameterFile(lasmerge.FILE5, self.tr("5th file")))
        self.addParameter(ParameterFile(lasmerge.FILE6, self.tr("6th file")))
        self.addParameter(ParameterFile(lasmerge.FILE7, self.tr("7th file")))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasmerge.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasmerge")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        file2 = self.parameterAsInt(parameters, lasmerge.FILE2)
        if file2 is not None:
            commands.append("-i")
            commands.append(file2)
        file3 = self.parameterAsInt(parameters, lasmerge.FILE3)
        if file3 is not None:
            commands.append("-i")
            commands.append(file3)
        file4 = self.parameterAsInt(parameters, lasmerge.FILE4)
        if file4 is not None:
            commands.append("-i")
            commands.append(file4)
        file5 = self.parameterAsInt(parameters, lasmerge.FILE5)
        if file5 is not None:
            commands.append("-i")
            commands.append(file5)
        file6 = self.parameterAsInt(parameters, lasmerge.FILE6)
        if file6 is not None:
            commands.append("-i")
            commands.append(file6)
        file7 = self.parameterAsInt(parameters, lasmerge.FILE7)
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
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'LAStools'

    def groupId(self):
        return 'LAStools'

    def createInstance(self):
        return laszip()
	