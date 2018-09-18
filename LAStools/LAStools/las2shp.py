# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2shp.py
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
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class las2shp(LAStoolsAlgorithm):

    POINT_Z = "POINT_Z"
    RECORD_SIZE = "RECORD_SIZE"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterBoolean(las2shp.POINT_Z, "use PointZ instead of MultiPointZ", False))
        self.addParameter(QgsProcessingParameterNumber(las2shp.RECORD_SIZE, "number of points per record", QgsProcessingParameterNumber.Integer, 1024, False, 0, 65536))
        self.addParametersGenericOutputGUI("Output SHP file", "shp", True)
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2shp")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        if (self.parameterAsBool(parameters, las2shp.POINT_Z, context)):
            commands.append("-single_points")
        record_size = self.parameterAsInt(parameters, las2shp.RECORD_SIZE, context)
        if (record_size != 1024):
            commands.append("-record_size")
            commands.append(unicode(record_size))
        self.addParametersGenericOutputCommands(parameters, context, commands, "-o")
        self.addParametersAdditionalCommands(parameters, context, commands)
        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2shp'

    def displayName(self):
        return 'las2shp'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return las2shp()
