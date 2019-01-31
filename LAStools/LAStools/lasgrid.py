# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgrid.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasgrid(LAStoolsAlgorithm):

    ATTRIBUTE = "ATTRIBUTE"
    METHOD = "METHOD"
    ATTRIBUTES = ["elevation", "intensity", "rgb", "classification"]
    METHODS = ["lowest", "highest", "average", "stddev"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParametersStepGUI()
        self.addParameter(QgsProcessingParameterEnum(lasgrid.ATTRIBUTE, "Attribute", lasgrid.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasgrid.METHOD, "Method", lasgrid.METHODS, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasgrid.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False))
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasgrid")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        self.addParametersStepCommands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, lasgrid.ATTRIBUTE, context)
        if (attribute != 0):
            commands.append("-" + lasgrid.ATTRIBUTES[attribute])
        method = self.parameterAsInt(parameters, lasgrid.METHOD, context)
        if (method != 0):
            commands.append("-" + lasgrid.METHODS[method])
        if (self.parameterAsBool(parameters, lasgrid.USE_TILE_BB, context)):
            commands.append("-use_tile_bb")
        self.addParametersRasterOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasgrid'

    def displayName(self):
        return 'lasgrid'

    def group(self):
        return 'file - raster derivatives'

    def groupId(self):
        return 'file - raster derivatives'

    def createInstance(self):
        return lasgrid()
