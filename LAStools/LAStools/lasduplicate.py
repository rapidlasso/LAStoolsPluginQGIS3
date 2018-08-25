# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasduplicate.py
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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from processing.core.parameters import ParameterFile


class lasduplicate(LAStoolsAlgorithm):

    LOWEST_Z = "LOWEST_Z"
    UNIQUE_XYZ = "UNIQUE_XYZ"
    SINGLE_RETURNS = "SINGLE_RETURNS"
    RECORD_REMOVED = "RECORD_REMOVED"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasduplicate')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.LOWEST_Z,
                                           self.tr("keep duplicate with lowest z coordinate"), False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.UNIQUE_XYZ,
                                           self.tr("only remove duplicates in x y and z"), False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.SINGLE_RETURNS,
                                           self.tr("mark surviving duplicate as single return"), False))
        self.addParameter(ParameterFile(lasduplicate.RECORD_REMOVED,
                                        self.tr("record removed duplicates to LAS/LAZ file")))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasduplicate")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        if self.parameterAsInt(parameters, lasduplicate.LOWEST_Z):
            commands.append("-lowest_z")
        if self.parameterAsInt(parameters, lasduplicate.UNIQUE_XYZ):
            commands.append("-unique_xyz")
        if self.parameterAsInt(parameters, lasduplicate.SINGLE_RETURNS):
            commands.append("-single_returns")
        record_removed = self.parameterAsInt(parameters, lasduplicate.RECORD_REMOVED)
        if record_removed is not None and record_removed != "":
            commands.append("-record_removed")
            commands.append(record_removed)
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
	