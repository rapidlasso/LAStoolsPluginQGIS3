# -*- coding: utf-8 -*-

"""
***************************************************************************
    shp2las.py
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
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class shp2las(LAStoolsAlgorithm):

    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI()
        self.addParametersGenericInputGUI("Input SHP file", "shp", False)
        self.addParameter(QgsProcessingParameterNumber(shp2las.SCALE_FACTOR_XY, "resolution of x and y coordinate", QgsProcessingParameterNumber.Double, 0.01, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(shp2las.SCALE_FACTOR_Z, "resolution of z coordinate", QgsProcessingParameterNumber.Double, 0.01, False, 0.0))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "shp2las")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersGenericInputCommands(parameters, context, commands, "-i")
        scale_factor_xy = self.parameterAsDouble(parameters, shp2las.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsInt(parameters, shp2las.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale_factor")
            commands.append(unicode(scale_factor_xy) + " " + unicode(scale_factor_xy) + " " + unicode(scale_factor_z))
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'shp2las'

    def displayName(self):
        return 'shp2las'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return shp2las()
