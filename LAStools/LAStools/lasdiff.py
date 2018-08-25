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
from LAStoolsUtils import LAStoolsUtils
from LAStoolsAlgorithm import LAStoolsAlgorithm

from processing.core.parameters import ParameterFile
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum


class lasdiff(LAStoolsAlgorithm):

    OTHER_POINT_FILE = "OTHER_POINT_FILE"
    CREATE_DIFFERENCE_FILE = "CREATE_DIFFERENCE_FILE"
    SHUTUP = "SHUTUP"
    SHUTUP_AFTER = ["5", "10", "50", "100", "1000", "10000", "50000"]

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasdiff')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(ParameterFile(lasdiff.OTHER_POINT_FILE,
                                        self.tr("other input LAS/LAZ file"), False, False))
        self.addParameter(QgsProcessingParameterEnum(lasdiff.SHUTUP,
                                             self.tr("stop reporting difference after this many points"), lasdiff.SHUTUP_AFTER, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasdiff.CREATE_DIFFERENCE_FILE,
                                           self.tr("create elevation difference file (if points are in the same order)"), False))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasdiff.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasdiff")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        file = self.parameterAsInt(parameters, lasdiff.OTHER_POINT_FILE)
        if file is not None:
            commands.append("-i")
            commands.append('"' + file + '"')
        shutup = self.parameterAsInt(parameters, lasdiff.SHUTUP)
        if (shutup != 0):
            commands.append("-shutup")
            commands.append(lasdiff.SHUTUP_AFTER[shutup])
        if self.parameterAsInt(parameters, lasdiff.CREATE_DIFFERENCE_FILE):
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
	