# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassort.py
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
from qgis.core import QgsProcessingParameterBoolean

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lassort(LAStoolsAlgorithm):

    BY_GPS_TIME = "BY_GPS_TIME"
    BY_RETURN_NUMBER = "BY_RETURN_NUMBER"
    BY_POINT_SOURCE_ID = "BY_POINT_SOURCE_ID"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterBoolean(lassort.BY_GPS_TIME, "sort by GPS time", False))
        self.addParameter(QgsProcessingParameterBoolean(lassort.BY_RETURN_NUMBER, "sort by return number", False))
        self.addParameter(QgsProcessingParameterBoolean(lassort.BY_POINT_SOURCE_ID, "sort by point source ID", False))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lassort")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lassort.BY_GPS_TIME, context)):
            commands.append("-gps_time")
        if (self.parameterAsBool(parameters, lassort.BY_RETURN_NUMBER, context)):
            commands.append("-return_number")
        if (self.parameterAsBool(parameters, lassort.BY_POINT_SOURCE_ID, context)):
            commands.append("-point_source")
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lassort'

    def displayName(self):
        return 'lassort'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lassort()
