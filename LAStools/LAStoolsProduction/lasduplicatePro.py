# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasduplicate.py
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


class lasduplicatePro(LAStoolsAlgorithm):

    LOWEST_Z = "LOWEST_Z"
    UNIQUE_XYZ = "UNIQUE_XYZ"
    SINGLE_RETURNS = "SINGLE_RETURNS"
    RECORD_REMOVED = "RECORD_REMOVED"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasduplicatePro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParameter(ParameterBoolean(lasduplicatePro.LOWEST_Z,
                                           self.tr("keep duplicate with lowest z coordinate"), False))
        self.addParameter(ParameterBoolean(lasduplicatePro.UNIQUE_XYZ,
                                           self.tr("only remove duplicates in x y and z"), False))
        self.addParameter(ParameterBoolean(lasduplicatePro.SINGLE_RETURNS,
                                           self.tr("mark surviving duplicate as single return"), False))
        self.addParameter(ParameterBoolean(lasduplicatePro.RECORD_REMOVED,
                                           self.tr("record removed duplicates"), False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasduplicate")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if self.getParameterValue(lasduplicatePro.LOWEST_Z):
            commands.append("-lowest_z")
        if self.getParameterValue(lasduplicatePro.UNIQUE_XYZ):
            commands.append("-unique_xyz")
        if self.getParameterValue(lasduplicatePro.SINGLE_RETURNS):
            commands.append("-single_returns")
        if self.getParameterValue(lasduplicatePro.RECORD_REMOVED):
            commands.append("-record_removed")
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
	
