# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasduplicatePro.py
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
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasduplicatePro(LAStoolsAlgorithm):

    LOWEST_Z = "LOWEST_Z"
    HIGHEST_Z = "HIGHEST_Z"
    UNIQUE_XYZ = "UNIQUE_XYZ"
    SINGLE_RETURNS = "SINGLE_RETURNS"
    NEARBY = "NEARBY"
    NEARBY_TOLERANCE = "NEARBY_TOLERANCE"
    RECORD_REMOVED = "RECORD_REMOVED"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterBoolean(lasduplicatePro.LOWEST_Z, "keep duplicate with lowest z coordinate", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicatePro.HIGHEST_Z, "keep duplicate with highest z coordinate", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicatePro.UNIQUE_XYZ, "only remove duplicates in x y and z", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicatePro.SINGLE_RETURNS, "mark surviving duplicate as single return", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicatePro.NEARBY, "keep only one point within specified tolerance ", False))
        self.addParameter(QgsProcessingParameterNumber(lasduplicatePro.NEARBY_TOLERANCE, "tolerance value", QgsProcessingParameterNumber.Double, 0.02, False, 0.001))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicatePro.RECORD_REMOVED, "record removed duplicates to LAS/LAZ file", False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasduplicate")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasduplicatePro.LOWEST_Z, context)):
            commands.append("-lowest_z")
        if (self.parameterAsBool(parameters, lasduplicatePro.HIGHEST_Z, context)):
            commands.append("-highest_z")
        if (self.parameterAsBool(parameters, lasduplicatePro.UNIQUE_XYZ, context)):
            commands.append("-unique_xyz")
        if (self.parameterAsBool(parameters, lasduplicatePro.SINGLE_RETURNS, context)):
            commands.append("-single_returns")
        if (self.parameterAsBool(parameters, lasduplicatePro.NEARBY, context)):
            commands.append("-nearby")
            commands.append(unicode(self.parameterAsDouble(parameters, lasduplicatePro.NEARBY_TOLERANCE, context)))
        if (self.parameterAsBool(parameters, lasduplicatePro.RECORD_REMOVED, context)):
            commands.append("-record_removed")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasduplicatePro'

    def displayName(self):
        return 'lasduplicatePro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasduplicatePro()
