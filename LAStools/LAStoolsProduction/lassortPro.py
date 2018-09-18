# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassortPro.py
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

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lassortPro(LAStoolsAlgorithm):

    BY_GPS_TIME = "BY_GPS_TIME"
    BY_RETURN_NUMBER = "BY_RETURN_NUMBER"
    BY_POINT_SOURCE_ID = "BY_POINT_SOURCE_ID"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterBoolean(lassortPro.BY_GPS_TIME, "sort by GPS time", False))
        self.addParameter(QgsProcessingParameterBoolean(lassortPro.BY_RETURN_NUMBER, "sort by return number", False))
        self.addParameter(QgsProcessingParameterBoolean(lassortPro.BY_POINT_SOURCE_ID, "sort by point source ID", False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lassort")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lassortPro.BY_GPS_TIME, context)):
            commands.append("-gps_time")
        if (self.parameterAsBool(parameters, lassortPro.BY_RETURN_NUMBER, context)):
            commands.append("-return_number")
        if (self.parameterAsBool(parameters, lassortPro.BY_POINT_SOURCE_ID, context)):
            commands.append("-point_source")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lassortPro'

    def displayName(self):
        return 'lassortPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lassortPro()
